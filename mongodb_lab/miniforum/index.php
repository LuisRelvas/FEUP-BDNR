<?php
require_once 'config.php';

$collection = getMongoDBConnection();
$topicId = isset($_GET['topic']) ? $_GET['topic'] : null;

// Display header
echo '<!DOCTYPE html>
<html>
<head>
    <title>MiniForum</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>MiniForum</h1>
            <a href="new_topic.html" class="btn">Create New Topic</a>
            <a href="index.php" class="btn">Home</a>
        </header>';

if ($topicId) {
    // Display a single topic and its comments
    try {
        $topic = $collection->findOne(['_id' => new MongoDB\BSON\ObjectId($topicId)]);
        
        if ($topic) {
            echo '<div class="topic">
                <h2>' . htmlspecialchars($topic['title']) . '</h2>
                <p>' . nl2br(htmlspecialchars($topic['body'])) . '</p>
                <p class="author">Posted by: ' . htmlspecialchars($topic['author']) . '</p>
            </div>';
            
            echo '<h3>Comments</h3>';
            
            if (isset($topic['comments']) && count($topic['comments']) > 0) {
                echo '<div class="comments">';
                foreach ($topic['comments'] as $comment) {
                    echo '<div class="comment">
                        <p>' . nl2br(htmlspecialchars($comment['text'])) . '</p>
                        <p class="author">Posted by: ' . htmlspecialchars($comment['author']) . '</p>
                    </div>';
                }
                echo '</div>';
            } else {
                echo '<p>No comments yet.</p>';
            }
            
            // Display comment form
            echo '<div class="comment-form">
                <h3>Add a Comment</h3>
                <form action="new_comment.php" method="post">
                    <input type="hidden" name="topic" value="' . $topicId . '">
                    <div class="form-group">
                        <label for="comment">Comment:</label>
                        <textarea name="comment" id="comment" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="author">Your Name:</label>
                        <input type="text" name="author" id="author" required>
                    </div>
                    <button type="submit" class="btn">Submit Comment</button>
                </form>
            </div>';
        } else {
            echo '<p>Topic not found.</p>';
        }
    } catch (Exception $e) {
        echo '<p>Error: ' . $e->getMessage() . '</p>';
    }
} else {
    // Display a list of all topics
    try {
        $topics = $collection->find();
        
        echo '<h2>All Topics</h2>';
        echo '<div class="topics-list">';
        
        foreach ($topics as $topic) {
            echo '<div class="topic-item">
                <a href="index.php?topic=' . $topic['_id'] . '">' . htmlspecialchars($topic['title']) . '</a>
                <p class="author">by ' . htmlspecialchars($topic['author']) . '</p>
            </div>';
        }
        
        echo '</div>';
    } catch (Exception $e) {
        echo '<p>Error: ' . $e->getMessage() . '</p>';
    }
}

echo '</div></body></html>';
?>