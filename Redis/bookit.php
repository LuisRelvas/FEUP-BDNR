<?php 

require 'vendor/autoload.php';


Predis\Autoloader::register();

try
{
    $redis = new Predis\Client();

    $new_url = $_POST['url']; 
    $tags = explode(' ', $_POST['tags']);

    $bookmark_id = $redis->incr("next_bookmark_id");

    $timestamp = time();

    $redis->hmset("bookmark:$bookmark_id", ['url' => $new_url]);

    $redis->zadd("bookmarks_by_time", [$bookmark_id => $timestamp]);

    foreach ($tags as $tag) {
        $redis->sadd("bookmark:$bookmark_id:tags", $tag);
        $redis->sadd("tag:$tag", $bookmark_id);
    }

    echo "URL: " . $new_url . " has been added to the database with tags: " . implode(', ', $tags);

    header('Location: index.php');

}
catch (Exception $e)
{
    echo "Couldn't connect to Redis";
    echo $e->getMessage();
}



?>