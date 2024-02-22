// import 'package:flutter/material.dart';

// void main() {
//   runApp(const MyApp());
// }

// class MyApp extends StatelessWidget {
//   const MyApp({super.key});

//   // This widget is the root of your application.
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Flutter Demo',
//       theme: ThemeData(
//         colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
//         useMaterial3: true,
//       ),
//       home: const MyHomePage(title: 'Flutter Demo Home Page'),
//     );
//   }
// }

import 'package:csn/screen/bus_schedule.dart';
import 'package:flutter/material.dart';

import 'screen/campus_map.dart';
import 'screen/home_screen.dart';

/// Flutter code sample for [NavigationBar].

void main() => runApp(const NavigationBarApp());

class NavigationBarApp extends StatelessWidget {
  const NavigationBarApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(useMaterial3: true),
      home: const NavigationExample(),
    );
  }
}

class NavigationExample extends StatefulWidget {
  const NavigationExample({super.key});

  @override
  State<NavigationExample> createState() => _NavigationExampleState();
}

class _NavigationExampleState extends State<NavigationExample> {
  int currentPageIndex = 1;

  @override
  Widget build(BuildContext context) {
    final ThemeData theme = Theme.of(context);
    return Scaffold(
      bottomNavigationBar: NavigationBar(
        // 콜백 메서드. 한 destination이 선택되었을 때 호출. selectedIndex값 업데이트. NavigationBar Rebuild
        onDestinationSelected: (int index) {
          setState(() {
            currentPageIndex = index; // 인덱스 변수 업데이트
          });
        },
        indicatorColor: Colors.amber,
        // 어떤 destination이 선택되었는지 결정
        selectedIndex: currentPageIndex, // 인덱스 변수
        // 아이콘 메뉴 (페이지 이동)
        destinations: const <Widget>[
          NavigationDestination(
            selectedIcon: Icon(Icons.departure_board),
            icon: Icon(Icons.departure_board_outlined),
            label: '셔틀 시간표',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.home), // 선택되었을 때의 아이콘
            icon: Icon(Icons.home_outlined),
            label: '홈',
          ),
          NavigationDestination(
            selectedIcon: Icon(Icons.map),
            icon: Icon(Icons.map_outlined),
            label: '캠퍼스 맵',
          ),
        ],
        // animationDuration: Duration(seconds: 5), // 알약 애니메이션 시간 조절
      ),
      body: <Widget>[
        const BusSchedule(),
        const HomeScreen(),
        const CampusMap(),
      ][currentPageIndex],
    );
  }
}
