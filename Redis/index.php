<?php 

require 'vendor/autoload.php';

Predis\Autoloader::register();

session_start(); 

try 
{
    $redis = new Predis\Client();

    echo "<a href='add.html'>Add Bookmark</a><br>";

    $tags = explode(',', $_GET['tags']);
    

    if ($tags[0] != "") { 
        echo "<h1>Bookmarks with tags: " . implode(', ', $tags) . "</h1>";
        echo "<p>Number of tags: " . count($tags) . "</p>";
        if(count($tags) > 1) 
        {
            for ($i = 0; $i < count($tags) - 1; $i++) {
                $bookmarks = $redis->sinter("tag:{$tags[$i]}", "tag:{$tags[$i + 1]}");
            }
        }
        else 
        {
            $bookmarks = $redis->smembers("tag:$tags[0]");
        }
        
    
        echo "<h1>Bookmarks</h1>";

        foreach ($bookmarks as $bookmark_id) {
            $url = $redis->hget("bookmark:$bookmark_id", 'url');
            echo "<a href='$url'>$url</a><br>";
            echo "Tags: ";
            $bookmarkTags = $redis->smembers("bookmark:$bookmark_id:tags");
            foreach ($bookmarkTags as $tag) {
                echo "<a href='index.php?tags=$tag'>$tag</a> ";
            }
            echo "<br>";
        }
    }
    else 
    {
        $bookmarks = $redis->zrevrange("bookmarks_by_time", 0, 15);

        echo "<h1>Bookmarks</h1>";
        foreach ($bookmarks as $bookmark_id) {
            $url = $redis->hget("bookmark:$bookmark_id", 'url');
            echo "<a href='$url'>$url</a><br>";
            echo "Tags: ";
            $bookmarkTags = $redis->smembers("bookmark:$bookmark_id:tags");
            foreach ($bookmarkTags as $tag) {
                echo "<a href='index.php?tags=$tag'>$tag</a> ";
            }
            echo "<br>";
        }
    }
    
}
catch (Exception $e)
{
    echo "Couldn't connect to Redis";
    echo $e->getMessage();
}


?>