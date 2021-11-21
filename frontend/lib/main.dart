import 'package:flutter/material.dart';

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
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {


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
            Text(
              'Place metadata here',
            ),
            Text(
              "Null"
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
