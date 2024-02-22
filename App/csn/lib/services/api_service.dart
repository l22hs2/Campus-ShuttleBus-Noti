import 'dart:convert'; //jsonDecode
import 'package:http/http.dart' as http;
import 'package:csn/models/shuttle_model.dart';

class ApiService {
  static const String baseUrl = 'http://132.145.80.50:8888/shuttle';

  static Future<List<ShuttleModel>> getShuttle() async {
    List<ShuttleModel> shuttleInstances = [];
    final url = Uri.parse(baseUrl);
    final response = await http.get(url);
    if (response.statusCode == 200) {
      final List<dynamic> shuttles =
          jsonDecode(utf8.decode(response.bodyBytes));
      for (var shuttle in shuttles) {
        final bus =
            ShuttleModel.fromJson(shuttle); // json 하나 씩 -> WebtoonModel 인스턴스화
        shuttleInstances.add(bus);
      }
      return shuttleInstances;
    }
    throw Error();
  }
}
