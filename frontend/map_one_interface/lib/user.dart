import 'dart:convert';
import 'package:async_builder/async_builder.dart';
import 'package:flutter/material.dart';
import 'package:map_one_interface/backendCalls.dart';
import 'package:map_one_interface/main.dart';
import 'package:http_requests/http_requests.dart';
import 'dart:math';

import 'loginPage.dart';

class user extends StatefulWidget
{

 // constructor
  user();

  _userState createState() => _userState();


}

class _userState extends State<user> 
{
  var photoArr = ['assets/images/curiosity.jpeg', 'assets/images/venus.jpeg',
  'assets/images/mars.jpeg', 'assets/images/titan.jpeg',
    'assets/images/uranus.jpeg',  ];

  // function: randomly selects a planetImage from photoArr
  // approach: randomly selects an index no larger than the length
  // of the arr
  randomlySelectPlanetImage(arr)
     {
       String returnStr;
       int maxInt = arr.length;
       int randomInt = Random().nextInt(maxInt);

       returnStr = arr[randomInt];

       return returnStr;
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
              const MaterialBanner(
                padding: EdgeInsets.all(20),
                content: Text('Hello, I am a Material Banner'),
                leading: Icon(Icons.agriculture_outlined),
                backgroundColor: Colors.green,
                actions: <Widget>[
                  TextButton(
                    onPressed: null,
                    child: Text('DISMISS'),
                  ),
                ],
              );
            },
            icon: FaceIcon,
            ),
          IconButton(
            onPressed:
                ()
            {
              //in order to change view, first the current
              // rendered context must be popped and then the
              // new one must be pushed onto the build stack
              Navigator.pop(context);
              Navigator.push(context, MaterialPageRoute(builder:
                  (context) => MapOne() ));

            },
            icon:HomeIcon,
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
        ], // Actions
        centerTitle: true,
      ),
      body: SafeArea(
          child: Column(
            children: [
              Container(
                decoration: BoxDecoration(
                    image: DecorationImage(
                        image: AssetImage(randomlySelectPlanetImage(photoArr)),
                        fit: BoxFit.fitWidth
                    )
                ),
                child: Container(
                  width: double.infinity,
                  height: 200,
                  child: Container(
                    alignment: Alignment(0.0,2.5),
                  ),
                ),
              ),
              SizedBox(
                height: 60,
              ),
              SizedBox(
                height: 10,
              ),
              Text(
                "version 0.25",
                style: TextStyle(
                    fontSize: 18.0,
                    color:Colors.grey,
                    letterSpacing: 2.0,
                    fontWeight: FontWeight.w300
                ),
              ),
              SizedBox(
                height: 10,
              ),

              Card(
                  margin: EdgeInsets.symmetric(horizontal: 20.0,vertical: 8.0),
                  elevation: 2.0,
                  child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 12,horizontal: 30),
                      child: Text("Access Saved Searches",style: TextStyle(
                          letterSpacing: 2.0,
                          fontWeight: FontWeight.w300
                      ),))
              ),
              Card(
                  margin: EdgeInsets.symmetric(horizontal: 20.0,vertical: 8.0),
                  elevation: 2.0,
                  child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 12,horizontal: 30),
                      child: Text("Export saved publications to .CSV format",style: TextStyle(
                          letterSpacing: 2.0,
                          fontWeight: FontWeight.w300
                      ),))
              ),

              Card(
                  margin: EdgeInsets.symmetric(horizontal: 20.0,vertical: 8.0),
                  elevation: 2.0,
                  child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 12,horizontal: 30),
                      child: Text("Change Password ",style: TextStyle(
                          letterSpacing: 2.0,
                          fontWeight: FontWeight.w300
                      ),))
              ),
              SizedBox(
                height: 15,
              ),
              Card(
                margin: EdgeInsets.symmetric(horizontal: 20.0,vertical: 8.0),
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Expanded(
                        child: Column(
                          children: [

                          ],
                        ),
                      ),

                    ],
                  ),
                ),
              ),

            ],

          //],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: null,
        tooltip: 'This page allows the user to make changes to their Mapone '
            'account as well. It also allows the user to export or view their search'
            'history ',

        child: Icon(Icons.info),
      ),

    );}


  }
  
