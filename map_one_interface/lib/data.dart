import 'dart:collection';
import 'dart:convert';
import 'dart:math';
import 'package:async_builder/async_builder.dart';
import 'package:flutter/material.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/main.dart';
import 'package:http_requests/http_requests.dart';

class data extends LinkedListEntry<data>
{

  var SourceArr = ["NAU", "USGS", "NASA","ASU", "UofA", "ESA", "Oxford"];
  var linkArr = ["xyz123.gov","clbj454.edu","pqwe.edu", "NAU.edu", "USGS.gov",
                 "ASU.edu"];
  var bodyArr = ["Mars","Venus","Mercury","Europa","Enceladus","Pluto", "Titan",
  "Triton"];
  var pubInfo = ["2003", "2021", "2022", "1999", "2012", "2017"];
  var author = ["Neil Armstrong","Carl Sagan","Buzz Aldrin"];
  var scale = ["1x", "4x", "2x"];
  


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
  var backendConsume;

  // rather than splicing an array to get the publication data
  // in an organized form I figured a linked list would be more
  // appropriate here
  final publicationNode = LinkedList<data>();

  // constructor
  data( String inTitle)
     {
      this.title = inTitle;
      backendConsume = backEndCalls(inTitle).consumeApi();
     }

     // Function: populateLL
     // approach: populates LL with serialized data
     populateLL(SerializedStr)
       {
         //serializedDt = serializeAsyncBuilderData(asyncStr);
       }

     // Function: iterateThroughLL
     // approach: iterate through data LL and splice data
     // into Source, Link, Body, Scale, Author and Publication Data.
     //
     iterateThrouhLL(serializedStr)
        {
          String link, body, scale, author, publicationData, serializedDt;


          if (publicationNode.isEmpty == true)
            {
              // populate LL

            }





        }

     // Function: serializeAsyncBuilderData
     //  Approach: convert async<String> into string
    //  by error handling "future" data
     serializeAsyncBuilderData(asyncStr)
        {
          String returnStr = " ";

          return returnStr;
        }

     // Function: fetchApiData
     // approach:
     AsyncBuilder<String> fetchApiData()
       {
        return AsyncBuilder<String>(
          future: backendConsume,
          waiting: (context) => Text('Loading...'),
          builder: (context, value) => Text('$value'),
          error: (context, error, stackTrace) => Text('Network Error $error'),
          );
       }
     // Function: populateDataRows
     // approach: returns DataRow object with parameters as values
  //link, body, scale, author, publicationData
       populateDataRows(ll)
       {
        var dataR;

           dataR = DataRow(
           cells: <DataCell>[
             DataCell(Text(randomlySelectDemoString(SourceArr))),
             DataCell(Text(randomlySelectDemoString(linkArr))),
             DataCell(Text(randomlySelectDemoString(bodyArr))),
             DataCell(Text(randomlySelectDemoString(scale))),
             DataCell(Text(randomlySelectDemoString(author))),
             DataCell(Text(randomlySelectDemoString(pubInfo))),
           ]
          );

          return dataR;

        }



}