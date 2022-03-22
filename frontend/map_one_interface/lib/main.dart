import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:async_builder/async_builder.dart';
import 'package:http_requests/http_requests.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/user.dart';
import 'backendCalls.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'entry.dart';
import 'package:syncfusion_flutter_datagrid/datagrid.dart';

Icon SearchIcon = const Icon(Icons.search);
Icon FaceIcon = const Icon(Icons.face);
Icon HomeIcon = const Icon(Icons.home);
Widget Bar = const Text("Enter the query for the desired publication");

// setting list to a string then spliting it into a new list on the main to call
// overflows for some reason
  // String entryIdArr = backEndCalls(entryIdArr) as String;
 //List EntryIdArr = entryIdArr.split(',');



    Future getApiEntries()
    async
    {
      // get request
      var response = await http.get(Uri.parse("https://mapone-api.herokuapp.com/entry/?action=0"));

      // store
      var decodedRes = json.decode(response.body).cast<Map<String,dynamic>>();

      List<Entry> responseList = await decodedRes.map<Entry>((json)=>
          Entry.fromJson(json)).toList();

      return responseList;

    }


   class EntryDataGridSource extends DataGridSource
      {
        EntryDataGridSource(this.entryList)
         {
          buildDataGridRow();
         }
        late List<DataGridRow> dataGridRows;
        late List<Entry> entryList;


        @override
        DataGridRowAdapter? buildRow(DataGridRow row)
         {
           return DataGridRowAdapter(cells: [
             Container(
               child: Text(row.getCells()[0].value.toString();
               overflow: TextOverflow.ellipsis,
               ),
               alignment: Alignment.centerLeft,
               padding: EdgeInsets.all(8.0),
             )
           ] );
         }
       List<DataGridRow> get rows => dataGridRows;

       void buildDataGridRow()
         {
          dataGridRows = entryList.map<DataGridRow>((dataGridRow){
            return DataGridRow(cells: [
              DataGridCell(columnName: 'entryID', value: dataGridRow.entry_id)
            ]);
            }).toList(growable: false);
          }

      }



  //Function: populateDataRows
  //approach: returns DataRow object with parameters as values
  //link, body, scale, author, publicationData
  populateDataRow()
  {
    var dataR;


    dataR = DataRow(
        cells: <DataCell>[
          DataCell(Text("")),
          DataCell(Text("Test")),
          DataCell(Text("")),
          DataCell(Text("Test")),
          DataCell(Text("Test")),
          DataCell(Text("Test")),]
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
                    populateDataRow()

                  ],
            ),

            Card(
                margin: EdgeInsets.symmetric(horizontal: 20.0,vertical: 8.0),
                elevation: 2.0,
                child: Padding(
                    padding: EdgeInsets.symmetric(vertical: 12,horizontal: 30),
                    child: Text(" ",style: TextStyle(
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