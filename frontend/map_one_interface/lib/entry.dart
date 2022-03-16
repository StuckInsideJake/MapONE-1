// entry class for all entry data
class Entry {
  final int entry_id;
  final String source_name;
  final String source_link;
  final String article_title;
  final String publication_date;
  final String author_list;
  final String map_body;

  Entry(
    {
      required this.entry_id,
      required this.source_name,
      required this.source_link,
      required this.article_title,
      required this.publication_date,
      required this.author_list,
      required this.map_body
    }
  );

  factory Entry.fromJson(Map<String, dynamic> json)
    {
      return Entry(
          entry_id: json['entry_id'],
          source_name: json['source_name'],
          source_link: json['source_link'],
          article_title: json['article_title'],
          publication_date: json['publication_date'],
          author_list: json['author_list'],
          map_body: json['map_body']
      );
    }
}
