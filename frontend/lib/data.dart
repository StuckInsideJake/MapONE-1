import 'dart:convert';
import 'package:async_builder/async_builder.dart';
import 'package:flutter/material.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/main.dart';
import 'package:http_requests/http_requests.dart';

class data
{
  String inData = "Rest data to be placed here for easy parsing";

  data(String inData)
     {
      this.inData = inData;
     }

     // Function: spliceInDt
     // approach: splice up inData into an array of
     // Strings in order to correspond each to a particular dataCell
     // within dataRow.
     spliceInDt()
        {
          //TODO: implement 
        }
     // Function: populateDataRows
     // approach: returns DataRow object with parameters as values
     populateDataRows(source, link, body, scale, author, publicationInfo)
       {
        return DataRow(
           cells: <DataCell>[
             DataCell(Text(source)),
             DataCell(Text(link)),
             DataCell(Text(body)),
             DataCell(Text(scale)),
             DataCell(Text(author)),
             DataCell(Text(publicationInfo)),

           ]
         );
        }



}