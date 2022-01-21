import 'dart:convert';
import 'package:async_builder/async_builder.dart';
import 'package:flutter/material.dart';
import 'package:map_one_interface/main.dart';
import 'package:http_requests/http_requests.dart';

class backEndCalls extends MyHomePage
{


  String title = "aloha";

  backEndCalls(this.title) : super(title: title)
    {

    }


  Future<String> consumeApi()
  async{
    Response publication = await HttpRequests.get('http://127.0.0.1:8000/');

    return publication.content;
  }
}
