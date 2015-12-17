<?php

require_once __DIR__ . '/../vendor/autoload.php';

date_default_timezone_set('Europe/Berlin');

use Silex\Provider\FormServiceProvider;
use Symfony\Component\Form\Extension\Core\Type\FileType;
use Symfony\Component\Form\Extension\Core\Type\FormType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\HttpFoundation\File\File;
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
    /** @var \Symfony\Component\HttpFoundation\File\UploadedFile[] */
    public $images;
}

/** @var \Symfony\Component\Form\FormFactory $formFactory */
$formFactory = $app['form.factory'];
$imageForm = $formFactory
    ->createNamedBuilder('', FormType::class, new ImageData(), ['csrf_protection' => false])
    ->add('name', TextType::class)
    ->add('original_image', FileType::class)
    ->add('operator', TextType::class)
    ->add('images', FileType::class, ['multiple' => true])
    ->getForm();

$app->get('/images', function() use($app, $images) {
    $image = $images->find();

    $images = [];
    while ($next = $image->getNext()) {
        $images[] = $next;
    }

    return new JsonResponse($images);
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

    $id = $gridfs->storeFile($data->original_image->getPathname(), ['filename' => $data->original_image->getClientOriginalName(), 'contentType' => $data->original_image->getClientMimeType()]);

    $imageFiles = [];
    foreach ($data->images as $imageFile) {
        $imageFiles[] = $gridfs->storeFile($imageFile->getPathname(), ['filename' => $imageFile->getClientOriginalName(), 'contentType' => $imageFile->getClientMimeType()]);
    }

    $insert = ['name' => $data->name, 'operator' => $data->operator, 'original_image' => $id, 'images' => $imageFiles];
    $images->insert($insert);

    return new JsonResponse($insert);
});

$app->run();
