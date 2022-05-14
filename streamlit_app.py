import streamlit as st
from google.cloud import firestore

# db = firestore.Client.from_service_account_json("firestore-key.json")
import json
key_dict = json.loads(st.secrets["textkey"])
key_dict = "{'type': 'service_account', 'project_id': 'streamlit-reddit-ebe13', 'private_key_id': 'fc647b06e9eeaf1df20c8d9cf3a1c49545054b78', 'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQDBYW5A55boyTfk\nVasIJnKGDe3HoEjWJqatWvaIHdv6WdhwlqWRfZiyJVfn1MQ2Kuef70hllIRZt/a2\nGlqLuEaFE6yulA57ad0HjtpnzmbhifdlqBE1W/+xkxEif7e2i/lJqao/6hoBDBYw\ntznZhicV4csVDeNMSDrlKqdjFD1W4zvaZvaLZ844uK6hR6DnGourMJkRGrcK8jQk\nUbltoJOIpQgdDsqaKyNKi4kvb4V/WicdOdWVc7z62REQIJbtg4zt2XiudeKQ5tG9\n+ML0AX98fqbu/mI871i0vLfhBrqoJ3mK1nHFu7PMCsPkCVzVHxiR/NpFtx2zV8oR\ntqi8L14pAgMBAAECgf8+aDdB5Z1jV/MLQXg5JNnqT5z5wqsULRg/WcqkxP4a+/1Z\nR0Snb0uX7fVBk1MlbERLQ6TzI0Nf5BPpUvXMB8oPqE4N1dO0gE8uA1881BbfmM0g\ndJhucQIxakkH/415JHdKlwNetqEtvd84N2DFCc69+Ir8GgwRnuhz4dzWS62RCyry\nkvxS+nHvEJ4Lv9PZFcmms7rsXzGHXhKw4+ol9clthUwqPCvjGsT23TjxBqGidxGu\nbzfS4dcOlMAMqaEo71sRwNGkWv25qsYjL5a4lU4OvDMMgIjHKdg0C6XCMIo8MC1W\n02JopT5UPRj2IxflaAa5hKC7ZxvRNH0yS3FBnoECgYEA/LMpNLYMw43UrGYBxxtR\nr8cayqzmEiTU7VJFJHAyxMr5C+5fWfgwnhHbTaUWPTTeN5NLU475iZM0m9fhOBqv\nx4lrwi508ZZmK2UdgSHh8C2s7uSvDoogkwa5lTXvYbABm9twfdNdrvHLhMvFdu0y\nCxGVjA3/7qWWDTd2byT4rWkCgYEAw+fzVqAedI1Rv64uVOyKGqEiad1ofpO1QoIC\n2wDP+kNAfJ00xo0wUDpJ6jwqKeQ9VOAdZwqo5VpAtf19DAUVaff/9C2OSr6Eri7W\n1nuaV0A8FZDWlWZhoUU0m6hyF0DGi28/WnTvLwV6FxH18787OWf+Th0tyZ1I+W0t\nW5HBUsECgYB9JhnNMjAGFVLzgp10x1HgVSIuqAxVhgox8qGtlyd9kOxgfVCZ1TH2\nxu8ueAkYjPtU2MzgeBmbidzvJa4zw/u0PZmxlKJ0F0FIUo6XKnmkImrX8UfFUqEp\nT5ZPkGOapLlXQAlpN2nZP4TEosqLyJMVKkM/FpvezAERUJuGFfBWqQKBgFJF4CDa\nH9As5U8NlHGf4SPr1esFy/OUjsP+m7pjrfRZOATddKOJ+edHg3E2kTKEouk5Mb/r\nbyDa9WA4s8JPhD27pCdk1mQ3fLs1+o2a3SeVV2ZrLGMT2x6CVOSmKjvvvTIjp0SS\n5TwnHa4Aof0aq4GhVeBySp9oSZROsITLQphBAoGBALu/n89cxNi7dKhWHj4hGhas\nlWyUa7uCq3PjdXWUkleKLCTmPLJZXS/b+FhZ7yaNK9ZX/n9BoiAhnWywPsH9bVyM\nHiQXETaR+kwyrbhXheTVbp8jQmaGOMkQ8JbrY0fPz0SG0PsOWGbGlMWhhpGD1mqd\nN24XdzDiU8n4ArSDP6OU\n-----END PRIVATE KEY-----\n', 'client_email': 'firebase-adminsdk-h9zlm@streamlit-reddit-ebe13.iam.gserviceaccount.com', 'client_id': '101786546231325142433', 'auth_uri': 'https://accounts.google.com/o/oauth2/auth', 'token_uri': 'https://oauth2.googleapis.com/token', 'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs', 'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-h9zlm%40streamlit-reddit-ebe13.iam.gserviceaccount.com'}"
st.subheader(key_dict)
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="streamlit-reddit")

# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post")

# Once the user has submitted, upload it to the database
if title and url and submit:
	doc_ref = db.collection("posts").document(title)
	doc_ref.set({
		"title": title,
		"url": url
	})
	st.subheader(f"我們收到囉")
