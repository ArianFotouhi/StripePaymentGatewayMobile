import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:webview_flutter/webview_flutter.dart';

// #docregion platform_imports
// Import for Android features.
import 'package:webview_flutter_android/webview_flutter_android.dart';
// Import for iOS features.
import 'package:webview_flutter_wkwebview/webview_flutter_wkwebview.dart';

import 'requester.dart';
import 'dart:convert';

import 'package:http/http.dart' as http;

void main() => runApp(const MaterialApp(home: WebViewExample()));




class WebViewExample extends StatefulWidget {
  const WebViewExample({super.key});

  @override
  State<WebViewExample> createState() => _WebViewExampleState();
}

class _WebViewExampleState extends State<WebViewExample> {
  late final WebViewController _controller;


  String initial_url = 'https://github.com/ArianFotouhi/';




  @override
  void initState()  {
    super.initState();






    // #docregion platform_features
    late final PlatformWebViewControllerCreationParams params;
    if (WebViewPlatform.instance is WebKitWebViewPlatform) {
      params = WebKitWebViewControllerCreationParams(
        allowsInlineMediaPlayback: true,
        mediaTypesRequiringUserAction: const <PlaybackMediaTypes>{},
      );
    } else {
      params = const PlatformWebViewControllerCreationParams();
    }

    final WebViewController controller =
    WebViewController.fromPlatformCreationParams(params);
    // #enddocregion platform_features


    controller
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))


      ..loadRequest(Uri.parse(initial_url));


    _controller = controller;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(
          actions: [
            ElevatedButton(onPressed: () async {
              // Example payload: {'key1': 'value1', 'key2': 'value2'}
              Map<String, dynamic> payload = {
                'username': 'chris_hall',
                'lounge_id': 'lg_12412',
                'from_date': '12/12/2023 10:00',
                'to_date': '12/12/2023 11:00',
                'price': 1500,
                'item': 'YYZ international lounge',
                'currency': 'usd',
              };

              String result = await fetchData(
                  'https://iegapp.pythonanywhere.com/get_link', payload);

              _controller.loadRequest(Uri.parse(result));

            },
              child: Text('Checkout'),
            ),
          ],
        ),
        body: WebViewWidget(controller: _controller)

        );
  }


}




