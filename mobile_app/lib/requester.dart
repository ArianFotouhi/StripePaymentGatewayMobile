import 'package:http/http.dart' as http;
import 'dart:convert';

Future<String> fetchData(String url, Map<String, dynamic> payload) async {
  final response = await http.post(
    Uri.parse(url),
    body: json.encode(payload),
    headers: {'Content-Type': 'application/json'},
  );

  if (response.statusCode == 200) {
    // If server returns an OK response, parse the response
    Map<String, dynamic> data = json.decode(response.body);

    // Check if 'data' key exists in the response
    if (data.containsKey('data')) {
      // Extract the value associated with the 'data' key
      var dataValue = data['data'];
      return '$dataValue';
    } else {
      return 'Error: Key "data" not found in the response';
    }
  } else {
    // If the server did not return a 200 OK response,
    // throw an exception.
    return 'Error: ${response.statusCode}';
  }
}