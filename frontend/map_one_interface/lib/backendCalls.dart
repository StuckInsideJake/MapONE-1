import 'dart:convert';
import 'dart:html';
import 'package:async_builder/async_builder.dart';
import 'package:flutter/material.dart';
import 'package:map_one_interface/main.dart';
import 'package:http_requests/http_requests.dart';
import 'package:http/http.dart' as http;



/*class backEndCalls extends MapOneHomePage
{
 // List entryIdArr = [];
  List SourceNameArr = [];
  List SourceListArr = [];
  List TitleArr = [];
  List AuthorList = [];
  List GlobalDataRowList = [];



  var globalPtr;
  String title = "MapOne";
  bool verboseFlag = true;
  //String inData;



  backEndCalls(this.title) : super(title: title)
    {
      getApiEntries();
    }

  backEndCalls1()
  {
    getApiEntries();
  }



   getApiEntries()
   async
     {

      Response publication = await HttpRequests.get("https://mapone-api.herokuapp.com/entry/?action=0");

      var publicationContent = publication.response;


      globalPtr = publicationContent;




      jsonDecode(publicationContent);

      serializeApiEntries(publicationContent);
     }

     serializeApiEntries(pubcontent)
         {

          pubcontent = globalPtr;

           String responseStr = pubcontent;

           int i= 0;
           entryIdArr.add(pubcontent);
           print(entryIdArr.elementAt(0));

// comment out if no work
          // while(i < responseStr.length)
           //    {
           //      if(responseStr[i] == "{")
            //       {
              //       print(responseStr[i+12]);
                //     entryIdArr.add(responseStr[i+12]);
                  //   print(responseStr.substring(i+28, i+38));
                //     print(responseStr.substring(i+125, i+140));
                //     SourceNameArr.add(responseStr.substring(i+28, i+38));
                 //    SourceListArr.add(responseStr.substring(i+54, i+120));
                  //   TitleArr.add(responseStr.substring(i+140, i+200));

                   //}
                 //i++;
                }



            //  }
          //populateDataTable(entryIdArr, SourceNameArr, SourceListArr, TitleArr);



     }
     //comment out if no work
   //Function: populateDataRows
   //approach: returns DataRow object with parameters as values
  //link, body, scale, author, publicationData
  populateDataRows()
  {
    var dataR;
    dataR = DataRow(
        cells: <DataCell>[
          DataCell(Text("")),
          DataCell(Text("")),
          DataCell(Text("")),
          DataCell(Text("")),
          DataCell(Text("")),
          DataCell(Text("")),]
    );

    return dataR;

  }*/





