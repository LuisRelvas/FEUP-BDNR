<!DOCTYPE html>
<html>
<head>
    <title>HOSTS</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>Hosts</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Host Since</th>
                <th>Response Time</th>
            </tr>
        </thead>
        <tbody>
            <?php
            $request_uri = $_SERVER['REQUEST_URI'];
            $url = parse_url($request_uri, PHP_URL_PATH);
            $url = explode('/', $url);
            $url[2] = isset($url[2]) ? $url[2] : 0; 
            $urlHosts = "http://localhost:5000/hosts/{$url[2]}"; // URL da API
            $json = file_get_contents($urlHosts);
            $host = json_decode($json, true);
            if ($host) {
                    echo "<tr>
                            <td>{$host['host_id']}</td>
                            <td>{$host['host_name']}</td>
                            <td>{$host['host_since']}</td>
                            <td>{$host['host_response_time']}</td>
                          </tr>";
            } else {
                echo "<tr><td colspan='7'>Nenhum dado encontrado.</td></tr>";
            }

            ?>
        </tbody>
    </table>
</body>

</html>
