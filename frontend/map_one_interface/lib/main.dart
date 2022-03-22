import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/cupertino.dart';
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
import "package:intl/intl.dart";

import 'loginPage.dart';

Icon SearchIcon = const Icon(Icons.search);
Icon FaceIcon = const Icon(Icons.face);
Icon HomeIcon = const Icon(Icons.home);
Widget Bar = const Text(" MapOne ");

// setting list to a string then spliting it into a new list on the main to call
// overflows for some reason
  // String entryIdArr = backEndCalls(entryIdArr) as String;
 //List EntryIdArr = entryIdArr.split(',');

    Future<EntryDataGridSource> getEntryDataSource() async{
      var entryList = await getApiEntries();
      return EntryDataGridSource(entryList);

    }
    List<GridColumn> getColumns()
      {
        List<GridColumn> columns;
       columns = <GridColumn>[
         GridColumn(columnName: "Entry ID",
           width: 70,
           label: Container(
               padding: EdgeInsets.all(8),
               alignment: Alignment.center,
               child: Text("Entry ID",
                   overflow: TextOverflow.clip, softWrap: true )
           ),
         ),
         GridColumn(columnName: "Body ",
           width: 70,
           label: Container(
               padding: EdgeInsets.all(8),
               alignment: Alignment.center,
               child: Text("Body",
                   overflow: TextOverflow.clip, softWrap: true )
           ),
         ),
         GridColumn(columnName: "Article Title",
           width: 150,
           label: Container(
               padding: EdgeInsets.all(8),
               alignment: Alignment.center,
               child: Text("Article Title",
                   overflow: TextOverflow.visible, softWrap: true )
           ),
         ),
         GridColumn(columnName: "Publication Date",
           width: 70,
           label: Container(
               padding: EdgeInsets.all(8),
               alignment: Alignment.center,
               child: Text("Publication Date",
                   overflow: TextOverflow.clip, softWrap: true )
           ),
         ),
         GridColumn(columnName: "Author(s)",
           width: 70,
           label: Container(
               padding: EdgeInsets.all(8),
               alignment: Alignment.center,
               child: Text("Author(s)",
                   overflow: TextOverflow.clip, softWrap: true )
           ),
         ),
         GridColumn(columnName: "URL",
           width: 150,
           label: Container(
               padding: EdgeInsets.all(8),
               alignment: Alignment.center,
               child: Text("URL",
                   overflow: TextOverflow.clip, softWrap: true )
           ),
         ),

       ];
       return columns;
      }
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
               child: Text(row.getCells()[0].value.toString(),
               overflow: TextOverflow.ellipsis,
               ),
               alignment: Alignment.center,
               padding: EdgeInsets.all(8.0),
             ),
             Container(
               child: Text(row.getCells()[1].value.toString(),
                 overflow: TextOverflow.ellipsis,
               ),
               alignment: Alignment.center,
               padding: EdgeInsets.all(8.0),
             ),
             Container(
               child: Text(row.getCells()[2].value.toString(),
                 overflow: TextOverflow.visible,
               ),
               alignment: Alignment.center,
               padding: EdgeInsets.all(8.0),
             ),
             Container(
               child: Text(row.getCells()[3].value.toString(),
                 overflow: TextOverflow.visible,
               ),
               alignment: Alignment.center,
               padding: EdgeInsets.all(8.0),
             ),
             Container(
               child: Text(row.getCells()[4].value.toString(),
                 overflow: TextOverflow.visible,
               ),
               alignment: Alignment.center,
               padding: EdgeInsets.all(8.0),
             ),
             Container(
               child: Text(row.getCells()[5].value.toString(),
                 overflow: TextOverflow.visible,
               ),
               alignment: Alignment.center,
               padding: EdgeInsets.all(8.0),
             )
           ] );
         }
       List<DataGridRow> get rows => dataGridRows;

       void buildDataGridRow()
         {
          dataGridRows = entryList.map<DataGridRow>((dataGridRow){
            return DataGridRow(cells: [
              DataGridCell(columnName: 'entryID', value: dataGridRow.entry_id),
              DataGridCell(columnName: 'Body', value: dataGridRow.map_body),
              DataGridCell(columnName: 'Title', value: dataGridRow.article_title),
              DataGridCell(columnName: 'Publication date', value: dataGridRow.publication_date),
              DataGridCell(columnName: 'Publication Authors', value: dataGridRow.author_list),
              DataGridCell(columnName: 'URL', value: dataGridRow.source_link),
            ]);
            }).toList(growable: false);
          }

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
      home: MapOneHomePage(title:'MapOne Demo'),
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
  Widget build(BuildContext context)
     {
      return SafeArea(child:

        Scaffold( appBar:
        AppBar(
          title: Bar,
          automaticallyImplyLeading: false,
          actions:
          [
            IconButton( icon: SearchIcon,
            onPressed: () {
              setState(() {
                if(SearchIcon.icon == Icons.search)
                  {
                   SearchIcon = const Icon(Icons.cancel);
                   Bar = const ListTile(leading:
                   Icon(
                     Icons.search,
                     color: Colors.white,
                     size: 28
                   ));
                  }
                else
                  {
                   SearchIcon = const Icon(Icons.search);
                   Bar = const Text("Search");
                  }
              });
        } ),
            // button for user page
            IconButton( icon: Icon(Icons.face),
              onPressed: (){
               setState(() {
                 Navigator.pop(context);
                 Navigator.push(context, MaterialPageRoute(builder:
                     (context) => user() ));
               });
              },
          ),
           IconButton(
               icon: Icon(Icons.home),
               onPressed: (){
                 setState(() {
                   Navigator.pop(context);
                   Navigator.push(context, MaterialPageRoute(builder: (context) => MapOne() ));
                 });
               }
           ),
            IconButton(
                icon: Icon(Icons.vpn_key_outlined),
                onPressed: (){
                  setState(() {
                    Navigator.pop(context);
                    Navigator.push(context, MaterialPageRoute(builder: (context) => login() ));
                  });
                }
            ),

          ],

        ),
        // Publication Data
        body: FutureBuilder(
        future: getEntryDataSource(),
        builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot){
          return snapshot.hasData
              ? SfDataGrid(source: snapshot.data, columns: getColumns())
              : Center(child: CircularProgressIndicator(strokeWidth: 3,) );
        },
      ),),);
     }

}