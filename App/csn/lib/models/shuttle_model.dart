class ShuttleModel {
  final String id, title;

  ShuttleModel.fromJson(Map<String, dynamic> json)
      : id = json['post_num'],
        title = json['title'];
}
