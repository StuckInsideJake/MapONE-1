import 'dart:collection';
import 'dart:convert';
import 'package:async_builder/async_builder.dart';
import 'package:flutter/material.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/main.dart';
import 'package:http_requests/http_requests.dart';

class data extends LinkedListEntry<data>
{

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
       populateDataRows()
       {
        var dataR;

           dataR = DataRow(
           cells: <DataCell>[
             DataCell(Text(title)),
             DataCell(Text(title)),
             DataCell(Text(title)),
             DataCell(Text(title)),
             DataCell(Text(title)),
             DataCell(Text(title)),
           ]
          );

          return dataR;

        }



}