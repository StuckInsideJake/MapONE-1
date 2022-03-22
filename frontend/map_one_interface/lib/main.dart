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

Icon SearchIcon = const Icon(Icons.search);
Icon FaceIcon = const Icon(Icons.face);
Icon HomeIcon = const Icon(Icons.home);
Widget Bar = const Text("Enter the query for the desired publication");

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
       return <GridColumn>[
         GridTextColumn(columnName: "Entry ID",
         width: 70,
         label: Container(
           padding: EdgeInsets.all(8),
           alignment: Alignment.centerLeft,
           child: Text("Entry ID",
           overflow: TextOverflow.clip, softWrap: true )
         ),
         )];
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
  Widget build(BuildContext context)
     {
      return SafeArea(child: Scaffold(body: FutureBuilder(
        future: getEntryDataSource(),
        builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot){
          return snapshot.hasData
              ? SfDataGrid(source: snapshot.data, columns: getColumns())
              : Center(child: CircularProgressIndicator(strokeWidth: 3,) );
        },
      ),),);
     }

}