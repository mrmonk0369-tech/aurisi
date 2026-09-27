import sys,io,base64
src,dst=sys.argv[1],sys.argv[2]
h=io.open(src,encoding='utf-8').read()
assert len(h.encode('utf-8'))==1945893, 'base size mismatch'
assert h.count('APP_VERSION="60.55"')==1
pairs=[
  (base64.b64decode('ZnVuY3Rpb24gbGxTeXMoKXs=').decode('utf-8'),
   base64.b64decode('' +
    'dmFyIExMX1NURVBTPXsKIEZPVU5EQVRJT046WydBbHBoYWJldCAmIGV2ZXJ5IGxldHRlciBzb3Vu' +
    'ZCcsJ1NpbGVudCBsZXR0ZXJzIOKAlCBldmVyeSBydWxlJywnVGhlIDEwMCB2aXRhbCB3b3Jkcycs' +
    'JzUwIHN1cnZpdmFsIHBocmFzZXMnLCdQcmVzZW50IHNpbXBsZSB0ZW5zZScsJ1ByZXNlbnQgY29u' +
    'dGludW91cycsJ0FydGljbGVzICYgZ2VuZGVyIHJ1bGVzJywnUXVlc3Rpb24gd29yZHMgJiBhc2tp' +
    'bmcnLCdOdW1iZXJzLCB0aW1lICYgZGF5cycsJ1Bhc3Qgc2ltcGxlIHRlbnNlJywnUGFzdCBjb250' +
    'aW51b3VzJywnRnV0dXJlOiB3aWxsICYgZ29pbmcgdG8nLCdQcm9ub3VucyAmIHBvc3Nlc3NpdmVz' +
    'JywnUHJlcG9zaXRpb25zIG9mIHBsYWNlICYgdGltZScsJ0FkamVjdGl2ZXMgJiB0aGVpciBvcHBv' +
    'c2l0ZXMnLCdGb29kICYgZHJpbmsgd29yZHMnLCdUcmF2ZWwgJiBkaXJlY3Rpb25zJywnSG9tZSAm' +
    'IGZhbWlseSB3b3JkcycsJ1dvcmsgJiBzdHVkeSB3b3JkcycsJ1RvcCAyMCBpZGlvbXMnLCdDb21t' +
    'b24gSW5kaWFuLXNwZWFrZXIgbWlzdGFrZXMnLCdQcm9udW5jaWF0aW9uIGRyaWxsOiBoYXJkIHNv' +
    'dW5kcycsJ0xpc3RlbmluZzogc2xvdyBuYXR1cmFsIHNlbnRlbmNlcycsJ1NoYWRvd2luZzogcmVw' +
    'ZWF0IGFmdGVyIG1lJywnUmVhZGluZzogc2hvcnQgcmVhbCBwYXNzYWdlJywnV3JpdGluZzogbXkg' +
    'ZGF5IGluIDUgc2VudGVuY2VzJywnU3BlYWtpbmc6IGludHJvZHVjZSBteXNlbGYnLCdTcGVha2lu' +
    'ZzogYXNrIGZvciBoZWxwJywnRm91bmRhdGlvbiByZXZpZXcnLCdGb3VuZGF0aW9uIGNoZWNrcG9p' +
    'bnQgdGVzdCddLAogSU1NRVJTSU9OOlsnUmVhbCBjb250ZW50OiBzaG9ydCBzdG9yeScsJ1BvZGNh' +
    'c3QgJiBuZXdzIGxpc3RlbmluZycsJ1NoYWRvdyB0aGUgbmV3cycsJ0hlYWRsaW5lICsgZmlyc3Qg' +
    'cGFyYWdyYXBoJywnV2F0Y2ggJiBkZXNjcmliZSBhIHNjZW5lJywnRGVzY3JpYmUgbXkgZGFpbHkg' +
    'cm91dGluZScsJ1JlYWQgJiByZXRlbGwnLCdXcml0ZTogbWVzc2FnZSB0byBhIGZyaWVuZCcsJ1Bo' +
    'b25lIGNvbnZlcnNhdGlvbiBwcmFjdGljZScsJ01hcmtldCAmIHNob3Agcm9sZXBsYXknLCdMaXN0' +
    'ZW4gJiB3cml0ZSBkaWN0YXRpb24nLCdTb25nOiBjYXRjaCB0aGUgbHlyaWNzJywnUmVhZCBhIHJl' +
    'Y2lwZScsJ0V4cGxhaW4gbXkgZmF2b3VyaXRlIGZvb2QnLCdEaXJlY3Rpb25zOiBnaXZlICYgZm9s' +
    'bG93JywnU21hbGwgdGFsazogd2VhdGhlciAmIHdlZWtlbmQnLCdPcGluaW9uczogYWdyZWUgJiBk' +
    'aXNhZ3JlZScsJ1Bhc3Qgc3Rvcnk6IG15IGJlc3QgbWVtb3J5JywnRnV0dXJlIHBsYW5zOiB3ZWVr' +
    'ZW5kJywnR3JhZGVkIHJlYWRlciBjaGFwdGVyJywnTGlzdGVuaW5nOiBuYXR1cmFsIHNwZWVkJywn' +
    'SWRpb20gb2YgdGhlIGRheScsJ1BocmFzYWwgdmVyYnMgJiBwYXR0ZXJucycsJ1dyaXRlOiBhIGNv' +
    'bXBsYWludCcsJ1JvbGVwbGF5OiBqb2IgaW50ZXJ2aWV3JywnU3Rvcnl0ZWxsaW5nOiBmYWlyeSB0' +
    'YWxlJywnV2VlayByZXZpZXcnLCdTcGVlZCByb3VuZDogNTAgcXVlc3Rpb25zJywnRXJyb3IgaHVu' +
    'dDogZml4IG1pc3Rha2VzJywnSW1tZXJzaW9uIGNoZWNrcG9pbnQgdGVzdCddLAogRkxVRU5DWTpb' +
    'J0NvbnZlcnNhdGlvbjogaW50cm9kdWNlIGxpa2UgYSBuYXRpdmUnLCdEZWJhdGU6IHBpY2sgYSBz' +
    'aWRlJywnVGVsbCBhIDItbWludXRlIHN0b3J5JywnVGhpbmsgYWxvdWQ6IGRlc2NyaWJlIG15IGRh' +
    'eScsJ09yZGVyICYgY29tcGxhaW4gYXQgYSByZXN0YXVyYW50JywnRnVsbCBtb2NrIGpvYiBpbnRl' +
    'cnZpZXcnLCdQaG9uZSBjYWxsOiBib29rICYgbmVnb3RpYXRlJywnRXhwbGFpbiBteSBqb2Igb3Ig' +
    'aG9iYnknLCdEaXNjdXNzIG5ld3MgJiBvcGluaW9ucycsJ0h1bW91cjogam9rZXMgJiB3b3JkcGxh' +
    'eScsJ0FjY2VudCBwb2xpc2g6IHJlY29yZCAmIGNvbXBhcmUnLCdGYXN0IGxpc3RlbmluZzogbm8g' +
    'cmVwZWF0cycsJ1N1bW1hcml6ZSBhIHZpZGVvJywnUGVyc3VhZGUgbWU6IHNhbGVzIHBpdGNoJywn' +
    'QXJndWUgYm90aCBzaWRlcycsJ1JhcGlkLWZpcmUgUSZBJywnRnJlZSB0YWxrOiBhbnkgdG9waWMn' +
    'LCdHcmFtbWFyOiBteSB3ZWFrIHNwb3RzJywnSWRpb21zIGluIHJlYWwgY29udmVyc2F0aW9uJywn' +
    'RXNzYXkgd2l0aCBhcmd1bWVudHMnLCdMb25nIGFydGljbGUgZmFzdCByZWFkaW5nJywnVHJhbnNs' +
    'YXRlLWZyZWUgdGhpbmtpbmcgZHJpbGwnLCdSb2xlcGxheTogZGlmZmljdWx0IGN1c3RvbWVyJywn' +
    'U3RvcnkgY2hhaW46IGNvbnRpbnVlIGl0JywnQ291cnNlIHJldmlldycsJ0Z1bGwgbW9jayBleGFt' +
    'OiA0IHBpbGxhcnMnLCdGaXggZm9zc2lsaXplZCBtaXN0YWtlcycsJ0ZpbmFsIHByb251bmNpYXRp' +
    'b24gdHVuZS11cCcsJ0NvbmZpZGVuY2UgZGF5OiBvbmx5IHdpbnMnLCdGSU5BTCBGTFVFTkNZIEVY' +
    'QU0nXQp9OwpmdW5jdGlvbiBsbFN0ZXBJZHgoKXt2YXIgZD1sbERheSgpO3ZhciBwaD1sbFBoYXNl' +
    'KGQpO3ZhciBvZmY9cGg9PT0nRk9VTkRBVElPTic/MDoocGg9PT0nSU1NRVJTSU9OJz8zMDo2MCk7' +
    'cmV0dXJuIE1hdGgubWluKE1hdGgubWF4KDEsZC1vZmYpLDMwKS0xfQpmdW5jdGlvbiBsbFN0ZXAo' +
    'KXt2YXIgcGg9bGxQaGFzZShsbERheSgpKTtyZXR1cm4gTExfU1RFUFNbcGhdW2xsU3RlcElkeCgp' +
    'XX0KZnVuY3Rpb24gbGxNYXN0ZXIoKXsKICB2YXIgcz1sbEh1YigpO2lmKCFzfHwhcy5hY3RpdmUp' +
    'cmV0dXJuO3ZhciBMPWxsTGFuZygpOwogIGNsb3NlTEwoKTsKICBxdWljaygnT05FLVNIT1QgTUFT' +
    'VEVSIEZPVU5EQVRJT04gZm9yICcrTC5uYW1lKycg4oCUIHRoZSAxMDAlIHN1cnZpdmFsIGtpdCBJ' +
    'IHdpbGwgcmV2aXNlIGZvciB0aGUgd2hvbGUgY291cnNlLiBUZWFjaCBpdCBBTEwgaW4gdGhpcyBz' +
    'aW5nbGUgbGVzc29uLCBpbiBjbGVhciBzZWN0aW9uczogKDEpIEFMUEhBQkVUICYgU09VTkRTOiBl' +
    'dmVyeSBsZXR0ZXIgYW5kIGtleSBsZXR0ZXItY29tYmluYXRpb24gd2l0aCBpdHMgc291bmQ7ICgy' +
    'KSBTSUxFTlQgTEVUVEVSUzogZXZlcnkgc2lsZW50LWxldHRlciBydWxlIHdpdGggZXhhbXBsZSB3' +
    'b3JkczsgKDMpIFRFTlNFUzogQUxMIGVzc2VudGlhbCB0ZW5zZXMg4oCUIG5hbWUsIHdoZW4gdG8g' +
    'dXNlLCBob3cgdG8gZm9ybSwgb25lIG1pbmkgZXhhbXBsZSBlYWNoOyAoNCkgVE9QIDUwIFBIUkFT' +
    'RVM6IHRoZSBtb3N0LXVzZWQgZXZlcnlkYXkgcGhyYXNlczsgKDUpIFRPUCAyMCBJRElPTVM6IGlk' +
    'aW9tcyBuYXRpdmVzIHJlYWxseSB1c2U7ICg2KSBDT1JFIEdSQU1NQVI6IHRoZSBydWxlcyB0aGF0' +
    'IGNvdmVyIG1vc3Qgc2VudGVuY2VzOyAoNykgVEhFIDEwMCBWSVRBTCBXT1JEUy4gVGlnaHQgc2Vj' +
    'dGlvbnMsIGJvbGQga2V5IGl0ZW1zLCBzaG9ydCBleGFtcGxlcy4gVGhpcyBpcyB0aGUgc2luZ2xl' +
    'IG1vc3QgaW1wb3J0YW50IGxlc3NvbiBvZiB0aGUgY291cnNlIOKAlCBjb21wbGV0ZSBhbmQgdW5m' +
    'b3JnZXR0YWJsZS4nKTsKICBzZXRUaW1lb3V0KGxsTWFyaywxNTAwKTsKfQpmdW5jdGlvbiBsbFN5' +
    'cygpew==').decode('utf-8')),
  (base64.b64decode('' +
    'dmFyIGJhc2U9J1RoaXMgaXMgbXkgRGF5ICcrZCsnLycrKEwuZGF5c3x8J+KInicpKycgJytMLm5h' +
    'bWUrJyBsZXNzb24gKCcrbGxQaGFzZShkKSsnIHBoYXNlKS4gJzs=').decode('utf-8'),
   base64.b64decode('' +
    'dmFyIGJhc2U9J1RoaXMgaXMgbXkgRGF5ICcrZCsnLycrKEwuZGF5c3x8J+KInicpKycgJytMLm5h' +
    'bWUrJyBsZXNzb24g4oCUIENVUlJFTlQgU1RFUDogJytsbFN0ZXAoKSsnLiAnOw==').decode('utf-8')),
  (base64.b64decode('Kydcbic7Cn0KZnVuY3Rpb24gbGxNaXNzaW9uKGtpbmQpew==').decode('utf-8'),
   base64.b64decode('' +
    'KydcbkNVUlJFTlQgU1RFUDogJytsbFN0ZXAoKSsnLiBCdWlsZCB0b2RheVwncyBsZXNzb24gYXJv' +
    'dW5kIHRoaXMgc3RlcCB0b3BpYy5cbic7Cn0KZnVuY3Rpb24gbGxNaXNzaW9uKGtpbmQpew==').decode('utf-8')),
  (base64.b64decode('' +
    'aWYoaXNOZXcpe3RvYXN0KCfwn4yNICcrTC5uYW1lKycg4oCUIERheSAxLiBXZWxjb21lIHRvIHlv' +
    'dXIgZmx1ZW5jeSBqb3VybmV5IScpO3NldFRpbWVvdXQobGxWaXRhbCw2MDApfQ==').decode('utf-8'),
   base64.b64decode('' +
    'aWYoaXNOZXcpe3RvYXN0KCfwn4yNICcrTC5uYW1lKycg4oCUIERheSAxLiBZb3VyIE1hc3RlciBG' +
    'b3VuZGF0aW9uIGxlc3NvbiBpcyBjb21pbmchJyk7c2V0VGltZW91dChsbE1hc3Rlciw2MDApfQ==').decode('utf-8')),
  (base64.b64decode('' +
    'aHRtbCs9JzxkaXYgY2xhc3M9ImxsLXBoYXNlIj7imqEgVEhFIDQgUElMTEFSUyDigJQgRVZFUlkg' +
    'REFZPC9kaXY+PGRpdiBjbGFzcz0ibGwtcGQiPicrbGxQaGFzZURlc2MocGgpKyc8L2Rpdj4nOw==').decode('utf-8'),
   base64.b64decode('' +
    'aHRtbCs9JzxkaXYgY2xhc3M9ImxsLXBoYXNlIj7imqEgVEhFIDQgUElMTEFSUyDigJQgRVZFUlkg' +
    'REFZPC9kaXY+PGRpdiBjbGFzcz0ibGwtcGQiPicrbGxQaGFzZURlc2MocGgpKyc8L2Rpdj4nOwog' +
    'ICAgdmFyIHNpPWxsU3RlcElkeCgpO3ZhciBwaEs9bGxQaGFzZShkKTsKICAgIGh0bWwrPSc8ZGl2' +
    'IGNsYXNzPSJsbC1zdGVwIj7wn5ONIFNURVAgJysoc2krMSkrJyBvZiAzMDogJytMTF9TVEVQU1tw' +
    'aEtdW3NpXSsnPC9kaXY+JzsKICAgIGh0bWwrPSc8ZGl2IGNsYXNzPSJsbC1yb2FkIj5ORVhUIOKG' +
    'kiAnK0xMX1NURVBTW3BoS11bTWF0aC5taW4oc2krMSwyOSldKycgwrcgJytMTF9TVEVQU1twaEtd' +
    'W01hdGgubWluKHNpKzIsMjkpXSsnPC9kaXY+Jzs=').decode('utf-8')),
  (base64.b64decode('' +
    'aHRtbCs9JzxkaXYgY2xhc3M9ImZlYXQtc2VjIj48Yj7imqEgUE9XRVIgVE9PTFM8L2I+JzsKICAg' +
    'IGh0bWwrPSc8ZGl2IGNsYXNzPSJsbC1yb3cgbGwtbGluayIgb25jbGljaz0ibGxWaXRhbCgpIj4=').decode('utf-8'),
   base64.b64decode('' +
    'aHRtbCs9JzxkaXYgY2xhc3M9ImZlYXQtc2VjIj48Yj7imqEgUE9XRVIgVE9PTFM8L2I+JzsKICAg' +
    'IGh0bWwrPSc8ZGl2IGNsYXNzPSJsbC1yb3cgbGwtbGluayIgb25jbGljaz0ibGxNYXN0ZXIoKSI+' +
    '8J+OkyBNYXN0ZXIgRm91bmRhdGlvbiDigJQgb25lLXNob3Qga2l0OiBsZXR0ZXJzLCBzaWxlbnQg' +
    'bGV0dGVycywgQUxMIHRlbnNlcywgcGhyYXNlcywgaWRpb21zPC9kaXY+JzsKICAgIGh0bWwrPSc8' +
    'ZGl2IGNsYXNzPSJsbC1yb3cgbGwtbGluayIgb25jbGljaz0ibGxWaXRhbCgpIj4=').decode('utf-8')),
  (base64.b64decode('LmxsLWNvdW50e2NvbG9yOiM4Yjk0YTg7Zm9udC1zaXplOjExcHg7').decode('utf-8'),
   base64.b64decode('' +
    'LmxsLXN0ZXB7bWFyZ2luLXRvcDo4cHg7YmFja2dyb3VuZDpyZ2JhKDI0NSwxNTgsMTEsLjA4KTti' +
    'b3JkZXI6MXB4IHNvbGlkIHJnYmEoMjQ1LDE1OCwxMSwuMzUpO2JvcmRlci1yYWRpdXM6MTBweDtw' +
    'YWRkaW5nOjEwcHggMTJweDtmb250LXNpemU6MTNweDtmb250LXdlaWdodDo3MDA7Y29sb3I6I2Y1' +
    'OWUwYn0ubGwtcm9hZHtjb2xvcjojOGI5NGE4O2ZvbnQtc2l6ZToxMXB4O21hcmdpbjo2cHggMCAw' +
    'IDJweH0ubGwtY291bnR7Y29sb3I6IzhiOTRhODtmb250LXNpemU6MTFweDs=').decode('utf-8')),
]
for i,(a,c) in enumerate(pairs):
    assert h.count(a)==1, 'anchor R%d missing or dup'%(i+1)
    h=h.replace(a,c)
hdr=base64.b64decode('djYwLjU1IExBTkdVQUdFIEhVQiDigJQgUFVSRSBJTU1FUlNJT04gRURJVElPTgB2NjAuNTYgTEFOR1VBR0UgSFVCIOKAlCBUT1AtVElFUiBTVEVQLUJZLVNURVAgRURJVElPTg==').decode('utf-8').split(chr(0))
h=h.replace(hdr[0],hdr[1])
h=h.replace('APP_VERSION="60.55"','APP_VERSION="60.56"')
out=h.encode('utf-8')
assert len(out)==1950110, 'output mismatch'
for m in ['LL_STEPS','llStep','llMaster','ONE-SHOT MASTER FOUNDATION','FINAL FLUENCY EXAM','llHub','APP_VERSION="60.56"']:
    assert m in h, 'missing '+m
io.open(dst,'w',encoding='utf-8').write(h)
print('build_v6056 OK ->',len(out))
