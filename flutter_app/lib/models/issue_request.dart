class IssueRequest {
  final String description;
  final String? logs;
  final String? imageBase64;
  final String? sessionId;

  IssueRequest({
    required this.description,
    this.logs,
    this.imageBase64,
    this.sessionId,
  });

  Map<String, dynamic> toJson() => {
    'description': description,
    if (logs != null) 'logs': logs,
    if (imageBase64 != null) 'image_base64': imageBase64,
    if (sessionId != null) 'session_id': sessionId,
  };
}
