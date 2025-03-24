<?php
// URL of the Flask API
$api_url = 'http://localhost:5000/bookmarks';

$tags = isset($_GET['tags']) ? urlencode($_GET['tags']) : '';
$api_url = "http://localhost:5000/bookmarks?tags=$tags";
$response = file_get_contents($api_url);


$bookmarks = json_decode($response, true);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Bookmarks</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f3f3f3;
            padding: 20px;
            color: #333;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .bookmark-card {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            width: 300px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s;
        }
        .bookmark-card:hover {
            transform: translateY(-5px);
        }
        .bookmark-card a {
            color: #4CAF50;
            text-decoration: none;
            word-break: break-word;
        }
        .bookmark-card a:hover {
            text-decoration: underline;
        }
        .tags {
            font-size: 14px;
            color: #666;
            margin-top: 10px;
        }
        .timestamp {
            font-size: 12px;
            color: #999;
            margin-top: 5px;
        }
    </style>
</head>
<body>

<h1>Bookmarks</h1>

<div class="container">
    <?php if (!empty($bookmarks)): ?>
        <?php foreach ($bookmarks as $bookmark): ?>
            <div class="bookmark-card">
                <div><strong>ID:</strong> <?php echo htmlspecialchars($bookmark['id']); ?></div>
                <div class="tags"><strong>Tags:</strong> 
                    <?php if (!empty($bookmark['tags']) && is_array($bookmark['tags'])): ?>
                        <?php foreach ($bookmark['tags'] as $tag): ?>
                            <span><?php echo htmlspecialchars($tag); ?></span>
                        <?php endforeach; ?>
                    <?php else: ?>
                        <span>No tags available</span>
                    <?php endif; ?>
                </div>
                <div class="timestamp"><strong></strong> <?php echo htmlspecialchars($bookmark['timestamp']); ?></div>
                <div style="margin-top: 15px;">
                    <a href="<?php echo htmlspecialchars($bookmark['url']); ?>" target="_blank">
                        <?php echo htmlspecialchars($bookmark['url']); ?>
                    </a>
                </div>
            </div>
        <?php endforeach; ?>
    <?php else: ?>
        <p>No bookmarks found.</p>
    <?php endif; ?>
</div>

</body>
</html>
