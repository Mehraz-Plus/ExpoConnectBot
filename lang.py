import polib


msg_en = {}
msg_fa = {}
msg_ar = {}
msg_cn = {}
for entry in polib.pofile('msg_en.po'):
    msg_en[entry.msgid] = entry.msgstr
for entry in polib.pofile('msg_fa.po'):
    msg_fa[entry.msgid] = entry.msgstr
for entry in polib.pofile('msg_ar.po'):
    msg_ar[entry.msgid] = entry.msgstr
for entry in polib.pofile('msg_cn.po'):
    msg_cn[entry.msgid] = entry.msgstr

def get(msg, lang='en'):
    if lang == 'fa':
        return msg_fa.get(msg)
    elif lang == 'ar':
        return msg_ar.get(msg)
    elif lang == 'cn':
        return msg_cn.get(msg)
    else:
        return msg_en.get(msg)