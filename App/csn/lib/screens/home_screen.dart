import 'package:csn/models/shuttle_model.dart';
import 'package:csn/services/api_service.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  HomeScreen({super.key});

  Future<List<ShuttleModel>> shuttles = ApiService
      .getShuttle(); // return 'shuttleInstances'. 인스턴스화 된 json 데이터 리스트

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: FutureBuilder(
          // Future가 완료되길 기다림
          future: shuttles,
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              return Column(
                children: [
                  // SizedBox(height: 50),
                  Expanded(child: makeList(snapshot)),
                ],
              );
            }
            return Center(
              child: CircularProgressIndicator(),
            );
          },
        ),
      ),
    );
  }

  ListView makeList(AsyncSnapshot<List<ShuttleModel>> snapshot) {
    return ListView.separated(
      padding: EdgeInsets.symmetric(vertical: 10, horizontal: 10),
      separatorBuilder: (context, index) => SizedBox(
        width: 40,
      ),
      // scrollDirection: Axis.horizontal, // 가로 스크롤
      itemCount:
          snapshot.data!.length, // 아이템 개수 설정. dart가 몇 개의 아이템을 build 할 건지 알게 됨.
      itemBuilder: (context, index) {
        // FutureBuilder와 유사. ListView.builder가 아이템을 build할 때 호출하는 함수
        // index: 생성. build되는 아이템의 인덱스
        var webtoon = snapshot.data![index];
        return Text(webtoon.title);
      },
    );
  }
}
