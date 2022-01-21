import 'package:flutter/material.dart';
import 'package:async_builder/async_builder.dart';
import 'package:http_requests/http_requests.dart';
import 'package:map_one_interface/backendCalls.dart';

Icon SearchIcon = const Icon(Icons.search);
Widget Bar = const Text("Enter the query for the desired publication");


void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'MapOne',
      theme: ThemeData(

        primaryColor: Colors.black,
      ),
      home: MyHomePage(title: 'MapOne Demo'),
    );
  }
}

class MyHomePage extends StatefulWidget {

  // init constructor
  MyHomePage({Key? key, required this.title}) : super(key: key);

  // def const
  MyHomePage.withoutTitle()
    {

    }



  String title = "Map One Alpha";
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  static String title = "Map One Alpha";
  var backendConsume = new backEndCalls(title).consumeApi();


  AsyncBuilder<String> fetchApiData()
  {

    return AsyncBuilder<String>(
      future: backendConsume,
      waiting: (context) => Text('Loading...'),
      builder: (context, value) => Text('$value'),
      error: (context, error, stackTrace) => Text('Still not loading $error'),
    );
  }

  void _incrementCounter() {
    setState(() {

    });
  }

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

                  //Db and or Django operations go here
                }
                else
                {
                  SearchIcon = const Icon(Icons.search);
                  Bar = const Text("En");
                }
              });
            },
            icon: SearchIcon,
          )
        ], // Actions
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            fetchApiData(),
            Text(
                " "
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: null,
        tooltip: 'info',
        child: Icon(Icons.info),
      ),

    );}
}
