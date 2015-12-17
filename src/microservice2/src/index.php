<?php

require_once __DIR__ . '/../vendor/autoload.php';

use Silex\Provider\FormServiceProvider;
use Symfony\Component\Form\Extension\Core\Type\FileType;
use Symfony\Component\Form\Extension\Core\Type\FormType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\HttpFoundation\File\File;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

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
    /** @var File[] */
    public $images;
}

/** @var \Symfony\Component\Form\FormFactory $formFactory */
$formFactory = $app['form.factory'];
$imageForm = $formFactory
    ->createNamedBuilder('', FormType::class, new ImageData(), ['csrf_protection' => false])
    ->add('name', TextType::class)
    ->add('original_image', FileType::class)
    ->add('operator', TextType::class)
//    ->add('images', FileType::class, ['multiple' => true])
    ->getForm();

$app->get('/images/{name}', function($name) use($app, $images) {
    $image = $images->findOne(['name' => $name]);

    return 'Hello ' . $app->escape($image['name']);
});

$app->match('/images', function (Request $request) use($images, $imageForm, $gridfs) {
    $imageForm->handleRequest($request);

    if (!$imageForm->isValid()) {
        return new Response('Invalid form structure.', 400);
    }

    /** @var ImageData $data */
    $data = $imageForm->getData();

    $id = $gridfs->storeFile($data->original_image->getPathname(), ['filename' => $data->original_image->getClientOriginalName(), 'contentType' => 'image/png']);

    $images->insert(['name' => $data->name, 'operator' => $data->operator, 'original_image' => $id]);

    $data->original_image = $id;
    return json_encode($data);
});

$app->run();
