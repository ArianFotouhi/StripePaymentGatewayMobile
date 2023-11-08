import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:http/http.dart' as http;

void main() => runApp(const MaterialApp(home: WebViewExample()));

class WebViewExample extends StatefulWidget {
  const WebViewExample({super.key});

  @override
  State<WebViewExample> createState() => _WebViewExampleState();
}

class _WebViewExampleState extends State<WebViewExample> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    _fetchLink();
  }

  Future<void> _fetchLink() async {
    // Replace with your server URL
    final serverUrl = 'http://127.0.0.1:5000';

    // Define the data you want to send
    final Map<String, dynamic> requestData = {
      'username': 'chris_benjamin',
      'lounge_id': 'lg_3124',
      'from_date': '11/11/2023 16:00',
      'to_date': '11/11/2023 20:00',
      'price': 1200,
      'item': 'YYZ International Lounge',
      'currency': 'usd',
    };

    final response = await http.post('$serverUrl/get_link', body: requestData);

    if (response.statusCode == 200) {
      final Map<String, dynamic> responseData = json.decode(response.body);
      final String link = responseData['data'];


      final PlatformWebViewControllerCreationParams params =
      PlatformWebViewControllerCreationParams();
      final WebViewController controller =
      WebViewController.fromPlatformCreationParams(params);

      setState(() {
        _controller = controller;
      });

      _controller
        ..setJavaScriptMode(JavaScriptMode.unrestricted)
        ..setBackgroundColor(const Color(0x00000000))
        ..loadUrl(link);
    } else {
      print('Failed to fetch the link: ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(),
      body: WebView(
        initialUrl: 'about:blank', // A blank page initially
        javascriptMode: JavascriptMode.unrestricted,
        onWebViewCreated: (controller) {
          _controller = controller;
        },
      ),
    );
  }
}
