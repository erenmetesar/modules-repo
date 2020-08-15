# Copyright (C) 2020 TeamDerUntergang.
#
# SedenUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SedenUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

""" Diğer kategorilere uymayan fazlalık komutların yer aldığı modül. """

import os
from gtts import gTTS
from gtts.lang import tts_langs
from telethon.tl.types import DocumentAttributeAudio
from nicegrill import utils


class TextToSpeech:

    TTS_LANG = "tr"

    async def ttsxxx(query):
        """ .tts komutu ile Google'ın metinden yazıya dönüştürme servisi kullanılabilir. """
        textx = await query.get_reply_message()
        message = utils.get_arg(query)
        if message:
            pass
        elif textx:
            message = textx.text
        else:
            await query.edit(
                "`Yazıdan sese çevirmek için bir metin gir.`")
            return

        try:
            gTTS(message, lang=TextToSpeech.TTS_LANG)
        except AssertionError:
            await query.edit(
                'Metin boş.\n'
                'Ön işleme, tokenizasyon ve temizlikten sonra konuşacak hiçbir şey kalmadı.'
            )
            return
        except ValueError:
            await query.edit('Bu dil henüz desteklenmiyor.')
            return
        except RuntimeError:
            await query.edit('Dilin sözlüğünü görüntülemede bir hata gerçekleşti.')
            return
        tts = gTTS(message, lang=TextToSpeech.TTS_LANG)
        tts.save("h.mp3")
        with open("h.mp3", "rb") as audio:
            linelist = list(audio)
            linecount = len(linelist)
        if linecount == 1:
            tts = gTTS(message, lang=TextToSpeech.TTS_LANG)
            tts.save("h.mp3")
        with open("h.mp3", "r"):
            await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
            os.remove("h.mp3")
            await query.delete()

    async def langxxx(message):
        lang = utils.get_arg(message)
        if lang:
            TextToSpeech.TTS_LANG = lang
            await message.edit("<i>Dil ayarlandı</i>")
        else:
            await message.edit("<i>Dil belirle moron</i>")