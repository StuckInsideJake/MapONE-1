import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:async_builder/async_builder.dart';
import 'package:http_requests/http_requests.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/user.dart';
import 'backendCalls.dart';
import 'data.dart';
import 'dart:convert';

Icon SearchIcon = const Icon(Icons.search);
Icon FaceIcon = const Icon(Icons.face);
Icon HomeIcon = const Icon(Icons.home);
Widget Bar = const Text("Enter the query for the desired publication");
// setting list to a string then spliting it into a new list on the main to call
// overflows for some reason
 //String entryIdArr = backEndCalls(entryIdArr) as String;
 //List EntryIdArr = entryIdArr.split(',');

class backEndCalls extends MapOneHomePage
{
  List entryIdArr = [];
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

}

void main() {


  runApp(MapOne());
}

class MapOne extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'MapOne',
      theme: ThemeData( colorScheme: ColorScheme.fromSwatch(primarySwatch: Colors.indigo)

      ),
      home: MapOneHomePage(title: 'MapOne Demo'),
    );
  }
}

class MapOneHomePage extends StatefulWidget {

  // init constructor
  MapOneHomePage({Key? key, inData, required this.title}) : super(key: key);

  // empty constructor
  MapOneHomePage2()
    {

    }

  @override
  String title = "Map One Alpha";
  _MapOneHomePageState createState() => _MapOneHomePageState();


}

  class _MapOneHomePageState extends State<MapOneHomePage> {

    backEndCalls  backendObjk = new backEndCalls("Map One Alpha");
    List <dynamic>  backendObj = new backEndCalls("Map One Alpha").entryIdArr;

    //backendObj;



    //backendObj.elementAt(0);



    //var j = backendObj;





  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Bar,
        automaticallyImplyLeading: false,
        actions: [
          IconButton(
            onPressed: () {
              setState(() {

                if(SearchIcon.icon == Icons.search)
                {
                  SearchIcon = const Icon(Icons.cancel);
                  Bar = const ListTile(
                      leading: Icon(
                          Icons.search,
                          color: Colors.white,
                          size: 28));
                  title: TextField( decoration: InputDecoration(
                      hintText: 'type in journal name...',
                      hintStyle: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontStyle: FontStyle.italic)));
                  border: InputBorder.none;
                  style: TextStyle(color: Colors.grey);
                }
                else
                {
                  SearchIcon = const Icon(Icons.search);
                  Bar = const Text("Enter your query");
                }
              });
            },
            icon: SearchIcon,
          ),
          IconButton(
            onPressed:
          ()
            {
              // in order to change view, first the current
              // rendered context must be popped and then the
              // new one must be pushed onto the build stack
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder:
                  (context) => user()));
            },
            icon: FaceIcon,
            ),
          IconButton(
            onPressed:
                ()
            {
              // in order to change view, first the current
              // rendered context must be popped and then the
              // new one must be pushed onto the build stack
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder:
                  (context) => MapOne()));
            },
            icon:HomeIcon,
          )
        ], // Actions
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            DataTable(
              columns: const <DataColumn>[
                DataColumn(
                  label: Text("Entry",
                  style: TextStyle(fontStyle: FontStyle.italic),

                  ),
                ),
                DataColumn(
                  label: Text("Link",
                  style: TextStyle(fontStyle: FontStyle.italic),

                ),
                ),
                DataColumn(
                  label: Text("Body",
                    style: TextStyle(fontStyle: FontStyle.italic),
                  ),
                ),
                DataColumn(
                  label: Text("",
                    style: TextStyle(fontStyle: FontStyle.italic),
                  ),
                ),
                DataColumn(
                  label: Text("Author",
                    style: TextStyle(fontStyle: FontStyle.italic),
                  ),
                ),
                DataColumn(
                  label: Text("Publisher",
                    style: TextStyle(fontStyle: FontStyle.italic),
                  ),
                ),
              ],
              rows:  <DataRow>
                  [
                    //backendObj.elementAt(0),


                  ],
            ),
            Card(
                margin: EdgeInsets.symmetric(horizontal: 20.0,vertical: 8.0),
                elevation: 2.0,
                child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 12,horizontal: 30),
                    child: Text("", style: TextStyle(
                        letterSpacing: 2.0,
                        fontWeight: FontWeight.w300
                    ),))
            ),
            Card(
                margin: EdgeInsets.symmetric(horizontal: 20.0,vertical: 8.0),
                elevation: 2.0,
                child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 12,horizontal: 30),
                    child: Text("Save selected publication to account",style: TextStyle(
                        letterSpacing: 2.0,
                        fontWeight: FontWeight.w300
                    ),))
            ),

            ]
          //],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: null,
        tooltip: 'This page allows the user to save ',
        child: Icon(Icons.info),
      ),
    );}
}