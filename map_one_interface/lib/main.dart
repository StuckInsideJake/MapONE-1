import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:async_builder/async_builder.dart';
import 'package:http_requests/http_requests.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/user.dart';

import 'data.dart';

Icon SearchIcon = const Icon(Icons.search);
Icon FaceIcon = const Icon(Icons.face);
Icon HomeIcon = const Icon(Icons.home);
Widget Bar = const Text("Enter the query for the desired publication");


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
      theme: ThemeData(

        primaryColor: Colors.black,
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

  String title = "Map One Alpha";
  @override
  _MapOneHomePageState createState() => _MapOneHomePageState();
}

  class _MapOneHomePageState extends State<MapOneHomePage> {

  static String title = "Map One Alpha";

  var backendConsume = new backEndCalls(title).consumeApi();
  DataRow dataRowObj = new data(title).populateDataRows(title);


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
                  (context) => MapOne() ));

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
                  label: Text("Source",
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
                  label: Text("Scale",
                    style: TextStyle(fontStyle: FontStyle.italic),
                  ),
                ),
                DataColumn(
                  label: Text("Author",
                    style: TextStyle(fontStyle: FontStyle.italic),
                  ),
                ),
                DataColumn(
                  label: Text("Publication Info",
                    style: TextStyle(fontStyle: FontStyle.italic),
                  ),
                ),
              ],

              rows:  <DataRow>
                  [
                   dataRowObj,
                   dataRowObj,
                   dataRowObj,
                   dataRowObj,
                   dataRowObj,
                  ],

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