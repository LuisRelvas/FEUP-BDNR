<!DOCTYPE html>
<html>
<head>
    <title>Listings</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>Listings</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>URL</th>
                <th>Name</th>
                <th>Description</th>
                <th>Host ID</th>
                <th>Host Name</th>
                <th>Price</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $url = 'http://localhost:5000/listings'; // URL da API
            $json = file_get_contents($url);
            $listings = json_decode($json, true);

            if ($listings) {
                foreach ($listings as $listing) {
                    echo "<tr>
                            <td>{$listing['id']}</td>
                            <td><a href='{$listing['listing_url']}' target='_blank'>Link</a></td>
                            <td>{$listing['name']}</td>
                            <td>{$listing['description']}</td>
                            <td>{$listing['host_id']}</td>
                            <td>{$listing['host_name']}</td>
                            <td>" . number_format($listing['price'], 2) . "</td>
                          </tr>";
                }
            } else {
                echo "<tr><td colspan='7'>Nenhum dado encontrado.</td></tr>";
            }
            ?>
        </tbody>
    </table>
</body>
</html>
