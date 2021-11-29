import 'dart:convert';

import 'package:http/http.dart' as http;

class backEndCalls
{
  // defualt constructor
  backEndCalls()
  {}

  //
  void consumeApi()
   async {
     var client = http.Client();
     try {
       var response = await client.post(
           // once Django is running on a server other than local host this will change
           Uri.https('127.0.1', 'whatsit/create'),
           body: {'source': 'link', 'body': 'publication info'});
       var decodedResponse = jsonDecode(utf8.decode(response.bodyBytes)) as Map;
       var uri = Uri.parse(decodedResponse['uri'] as String);

   } finally {
   client.close();
   }
   }










}
