import 'dart:collection';
import 'dart:convert';
import 'dart:math';
import 'package:async_builder/async_builder.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/main.dart';
import 'package:http_requests/http_requests.dart';
import 'dart:developer' as developer;
import 'dart:io';




class data extends LinkedListEntry<data>
{

  var backendConsume;



  // function: randomly selects a planetImage from photoArr
  // approach: randomly selects an index no larger than the length
  // of the arr
  randomlySelectDemoString(arr)
  {
    String returnStr;
    int maxInt = arr.length;
    int randomInt = Random().nextInt(maxInt);

    returnStr = arr[randomInt];

    return returnStr;
  }

  // member dat
  String title = "Map one alpha";


  // rather than splicing an array to get the publication data
  // in an organized form I figured a linked list would be more
  // appropriate here
  final publicationNode = LinkedList<data>();

  // constructor
  data( String inTitle)
     {
      this.title = inTitle;

      var apiEntryNums = backEndCalls(inTitle).getApiEntries();
      print("data.dart call");


     }



     // Function: populateDataRows
     // approach: returns DataRow object with parameters as values
  //link, body, scale, author, publicationData
       populateDataRows()
       {
        var dataR;


           dataR = DataRow(
           cells: <DataCell>[
             DataCell(Text("")),
             DataCell(Text("")),
             DataCell(Text(" ")),
             DataCell(Text(" ")),
             DataCell(Text(" ")),
             DataCell(Text(" ")),
           ]
          );

          return dataR;

        }



}