<?php

$filename = __DIR__.preg_replace('#(\?.*)$#', '', $_SERVER['REQUEST_URI']);
if (php_sapi_name() === 'cli-server' && is_file($filename)) {
    return false;
}

require_once __DIR__ . '/../vendor/autoload.php';

date_default_timezone_set('Europe/Berlin');

use Silex\Provider\FormServiceProvider;
use Symfony\Component\Form\Extension\Core\Type\FileType;
use Symfony\Component\Form\Extension\Core\Type\FormType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

const MONGO_SERVER = 'mongodb://localhost:27017/evs';

// Init MongoDB.
$mongo = new MongoClient(MONGO_SERVER);

/** @var MongoDB $database */
$database = $mongo->evs;
/** @var MongoCollection $images */
$images = $database->images;
/** @var MongoGridFS $gridfs */
$gridfs = $database->getGridFS();

// Init HTTP.
$app = new Silex\Application();
$app['debug'] = true;
$app->register(new FormServiceProvider());

class ImageData {
    /** @var string */
    public $name;
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile */
    public $original_image;
    /** @var string */
    public $operator;
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile */
    public $combined;
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile */
    public $directions;
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile */
    public $imag;
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile */
    public $real;
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile */
    public $magnitudes;
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile */
    public $date;

    public static function fromDb(Request $request, array $data)
    {
        $imageData = new ImageData();
        $imageData->name = $data['name'];
        $imageData->operator = $data['operator'];

        /** @var MongoDate $date */
        $date = $data['date'];
        $imageData->date = $date->toDateTime()->getTimestamp() * 1000;

        $keys = [
            'original_image',
            'combined',
            'directions',
            'imag',
            'real',
            'magnitudes',
        ];

        foreach ($keys as $key) {
            $imageData->$key = $request->getSchemeAndHttpHost() . '/files/' . $data[$key]->{'$id'};
        }

        return $imageData;
    }
}

/** @var \Symfony\Component\Form\FormFactory $formFactory */
$formFactory = $app['form.factory'];
$imageForm = $formFactory
    ->createNamedBuilder('', FormType::class, new ImageData(), ['csrf_protection' => false])
    ->add('name', TextType::class)
    ->add('original_image', FileType::class)
    ->add('operator', TextType::class)
    ->add('combined', FileType::class)
    ->add('directions', FileType::class)
    ->add('imag', FileType::class)
    ->add('real', FileType::class)
    ->add('magnitudes', FileType::class)
    ->getForm();

$app->get('/images', function(Request $request) use($app, $images) {
    $image = $images->find()->sort(['date' => -1]);

    $images = [];
    while ($next = $image->getNext()) {
        $images[] = ImageData::fromDb($request, $next);
    }

    return new JsonResponse($images, 200, ['Access-Control-Allow-Origin' => '*']);
});

$app->get('/files/{id}', function($id) use($app, $images, $gridfs) {
    $file = $gridfs->findOne(['_id' => new MongoId($id)]);

    if ($file === null) {
        throw new NotFoundHttpException('File not found');
    }

    return new Response($file->getBytes(), 200, ['Content-type' => $file->file['contentType']]);
});

$app->get('/images/{name}', function($name) use($app, $images, $gridfs) {
    $image = $images->findOne(['name' => $name]);

    $cursor = $gridfs->find(['_id' => $image['original_image']]);

    $file = $cursor->getNext();
    return new Response($file->getBytes(), 200, ['Content-type' => $file->file['contentType']]);
});

$app->post('/images', function (Request $request) use($images, $imageForm, $gridfs) {
    $imageForm->handleRequest($request);

    if (!$imageForm->isValid()) {
        return new Response('Invalid form structure.', 400);
    }

    /** @var ImageData $data */
    $data = $imageForm->getData();

    /** @var MongoId $id */
    $id = $gridfs->storeFile($data->original_image->getPathname(), ['filename' => $data->original_image->getClientOriginalName(), 'contentType' => $data->original_image->getClientMimeType()]);
    $magnitudes_id = $gridfs->storeFile($data->magnitudes->getPathname(), ['filename' => $data->magnitudes->getClientOriginalName(), 'contentType' => $data->magnitudes->getClientMimeType()]);
    $directions_id = $gridfs->storeFile($data->directions->getPathname(), ['filename' => $data->directions->getClientOriginalName(), 'contentType' => $data->directions->getClientMimeType()]);
    $real_id = $gridfs->storeFile($data->real->getPathname(), ['filename' => $data->real->getClientOriginalName(), 'contentType' => $data->real->getClientMimeType()]);
    $imag_id = $gridfs->storeFile($data->imag->getPathname(), ['filename' => $data->imag->getClientOriginalName(), 'contentType' => $data->imag->getClientMimeType()]);
    $combined_id = $gridfs->storeFile($data->combined->getPathname(), ['filename' => $data->combined->getClientOriginalName(), 'contentType' => $data->combined->getClientMimeType()]);

    $insert = [
        'name' => $data->name,
        'operator' => $data->operator,
        'original_image' => $id,
        'magnitudes' => $magnitudes_id,
        'directions' => $directions_id,
        'real' => $real_id,
        'imag' => $imag_id,
        'combined' => $combined_id,
        'date' => new \MongoDate()
    ];
    $images->insert($insert);

    return new JsonResponse($insert);
});

$app->run();
