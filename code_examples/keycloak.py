import jwt
public_key = b"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu36daeJnuzefMaqWyOjkW664OLIx7MPrjSRkSX663YkqlLORiwFQX7NAbFIdV7VYpHe1uSi9caAEvqbQnzsVQtmBMWaZ+USNct3tm8jIn0GrnxrDGcQnYa4Gz2RhbMMDBdd42dBXwa+mIUWjCNigyBfU3W38lMd9p7cZzFvEOJCHC9EUf4DyeJo+SAVWP80kRU+7xspFYZzBoqSU0gNKY/aDmiOYVdPcx6U82REs7KyFQo0BHpiv0sJz6KftnmulMrJHoid115Y8Unm0yyJmlUlPIZJlaLXuqsWv7yiMtjNUq4CPvTH4hQSFJ7tFQhISXtdfrGU5vgk/Zs/PXzmv2QIDAQAB\n-----END PUBLIC KEY-----"
token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJLbnc3UFRMNmpkNXZDenpySVJpTDNycVpVZXRSN3Znb2ExaGdKbFo4Z24wIn0.eyJleHAiOjE3MzM4Njc4MjcsImlhdCI6MTczMzg2NzUyNywianRpIjoiY2YzMjU0MzMtZTliOS00ZjQ0LWI2MDQtMTc4MGRkMzliNWUwIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwL3JlYWxtcy9jb2RlZmxpeCIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJjOGM2ZTA1ZC03YTlkLTQwMmMtOGYzZC1mNDUyNzk2ZjZhODEiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJjb2RlZmxpeC1mcm9udGVuZCIsInNpZCI6ImY3NGY4ZWNkLTAyMDItNDI5Zi1hNWEyLTMxMTE5N2U5MjhiNCIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiLyoiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLWNvZGVmbGl4Il19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJhZG1pbiBhZG1pbiIsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIiwiZ2l2ZW5fbmFtZSI6ImFkbWluIiwiZmFtaWx5X25hbWUiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5AYWRtaW4uY29tIn0.sJfcrHs3CHScyia2hmgZnXuIRTAWMzysMNA7ws6a_0Fg4p8XC4bJ6bFTLcJr-FXUYyBPCcbS0Zk_RRzxtNsaAXCJ1B0C-MwPA_LWrgLjNpLDlEzenXqmvdfqHzJKmKHi6yKeEYA50yLrJ1xsFxJ2S6r4fvzabav7lGl1mOXnbWWZpg-w2Aocs5v5nq8b2W0bvAwc-JswqKaTR0L7xgf4O3YWviVWa-7tFl0xV_d2MfIPjY7BgdpSQweSd1cmDE8e-kdVZ3TEri7N39DW1qqSYGyL_GxDO4Y3-d8EaK8oAvCGKL2oZAlJxT-KohFESlMMfsTYSgj_O_GN6h2zMS5MWg"
decoded = jwt.decode(token, public_key, algorithms=['RS256'], audience='account')
