# 🎵 Music Generator - Gerador de Músicas Programático

Crie batidas de **funk** e **pop** completas com vozes sintetizadas usando Python!

Este projeto permite gerar músicas programaticamente, incluindo:
- 🥁 **Batidas** (funk carioca, pop moderno)
- 🎤 **Vozes** (TTS e melodias vocais)
- 🎹 **Melodias e harmonias**
- 🎼 **Composições completas** com estrutura (intro, verse, chorus)

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- FFmpeg (necessário para o pydub)

### Windows - Instalar FFmpeg
```powershell
# Via Chocolatey (recomendado)
choco install ffmpeg

# OU baixe manualmente de: https://ffmpeg.org/download.html
```

### Instalar dependências Python
```bash
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
music/
├── src/
│   ├── beat_generator.py      # Gerador de batidas e samples
│   ├── voice_generator.py     # Gerador de vozes e melodias
│   └── music_composer.py      # Compositor completo (combina tudo)
├── output/                     # Arquivos gerados (MP3, WAV, MIDI)
├── samples/                    # Samples de áudio (kick, snare, hihat)
├── requirements.txt            # Dependências
└── README.md
```

## 🎮 Como Usar

### 1️⃣ Gerar Batidas MIDI

```bash
cd src
python beat_generator.py
```

**Saída:**
- `output/funk_beat.mid` - Padrão de funk
- `output/pop_beat.mid` - Padrão pop
- `samples/kick_808.wav` - Sample de kick 808
- `samples/snare.wav` - Sample de snare
- `samples/hihat.wav` - Sample de hi-hat

### 2️⃣ Gerar Vozes

```bash
python voice_generator.py
```

**Saída:**
- `output/vocals_english.mp3` - Voz em inglês (TTS)
- `output/vocals_portuguese.mp3` - Voz em português (TTS)
- `output/vocal_melody.wav` - Melodia vocal sintética
- `output/vocal_chop.wav` - Vocal chop (estilo EDM/pop)
- `output/pop_melody.wav` - Melodia pop

### 3️⃣ Criar Música Completa

```bash
python music_composer.py
```

**Saída:**
- `output/funk_complete.mp3` - Faixa funk com melodia
- `output/pop_complete.mp3` - Faixa pop com vocais
- `output/full_song_structured.mp3` - Música completa estruturada

## 💻 Exemplos de Código

### Criar uma batida de funk

```python
from beat_generator import BeatGenerator

# Criar gerador
beat = BeatGenerator(tempo=128)

# Gerar padrão de funk
beat.create_funk_pattern(bars=8)
beat.add_bassline(pattern='funk', bars=8)

# Salvar MIDI
beat.save_midi('minha_batida.mid')
```

### Gerar voz a partir de texto

```python
from voice_generator import VoiceGenerator

vg = VoiceGenerator()

# Texto para voz em português
vg.text_to_speech(
    "Essa é a batida do futuro",
    language='pt-br',
    filename='minha_voz.mp3'
)
```

### Criar melodia vocal

```python
from voice_generator import VoiceGenerator

vg = VoiceGenerator()

# Notas MIDI (C, D, E, F, G)
notes = [60, 62, 64, 65, 67]
# Durações em milissegundos
durations = [300, 300, 300, 300, 600]

vg.create_vocal_melody(notes, durations, 'melodia.wav')
```

### Compor música completa

```python
from music_composer import MusicComposer

composer = MusicComposer(tempo=120)

# Criar faixa pop
track = composer.build_audio_track(style='pop', duration_seconds=30)

# Adicionar vocais
track = composer.add_vocals(track, "This is amazing", start_time=4000)

# Adicionar melodia
notes = [60, 64, 67, 64, 60]
durations = [400, 400, 400, 400, 800]
track = composer.add_melody(track, notes, durations, start_time=0)

# Exportar
composer.export_track(track, 'minha_musica', format='mp3')
```

## 🎯 Recursos

### Beat Generator
- ✅ Padrões de funk carioca
- ✅ Padrões de pop moderno
- ✅ Síntese de samples (kick 808, snare, hi-hat)
- ✅ Exportação MIDI
- ✅ Linhas de baixo personalizáveis

### Voice Generator
- ✅ Text-to-Speech (Google TTS)
- ✅ Suporte a português e inglês
- ✅ Melodias vocais sintéticas
- ✅ Vocal chops (efeito de corte rítmico)
- ✅ Conversão MIDI → Hz

### Music Composer
- ✅ Construção de faixas completas
- ✅ Mixagem de beats + vozes + melodias
- ✅ Estrutura de música (intro, verse, chorus, outro)
- ✅ Normalização e compressão automática
- ✅ Exportação em MP3/WAV

## 🔧 Personalização

### Mudar o BPM (tempo)

```python
composer = MusicComposer(tempo=140)  # Mais rápido
```

### Criar padrão personalizado

```python
beat = BeatGenerator(tempo=128)

# Seu padrão de kick personalizado
for i in range(8):
    beat.midi.addNote(0, 0, 36, i*0.5, 0.25, 100)

beat.save_midi('custom_beat.mid')
```

### Adicionar harmonia vocal

```python
vg = VoiceGenerator()

# Criar melodia base
vg.create_vocal_melody([60, 64, 67], [400, 400, 800], 'base.wav')

# Adicionar harmonia (terças e quintas)
harmony = vg.create_harmony('base.wav', intervals=[0, 4, 7])
harmony.export('harmony.wav', format='wav')
```

## 🎓 Próximos Passos

### Melhorias Sugeridas
1. **Adicionar mais estilos** (trap, house, techno)
2. **Implementar autotune real** (usando librosa/pyrubberband)
3. **Adicionar efeitos** (reverb, delay, chorus)
4. **Integrar IA para geração** (Bark, MusicGen, Stable Audio)
5. **Interface gráfica** (Tkinter ou web com Flask)
6. **Exportar para DAW** (Ableton Live Set, FL Studio)

### Recursos Avançados (Opcional)

Adicione ao `requirements.txt` e descomente:

```bash
# Análise e manipulação avançada de áudio
pip install librosa soundfile scipy

# Pitch shifting de qualidade
pip install pyrubberband

# Geração de música com IA (requer GPU)
pip install audiocraft transformers torch
```

## 📚 Referências

- **MIDI**: [MIDIUtil Documentation](https://midiutil.readthedocs.io/)
- **Audio**: [Pydub Documentation](https://github.com/jiaaro/pydub)
- **TTS**: [gTTS Documentation](https://gtts.readthedocs.io/)
- **Music Theory**: [music21](http://web.mit.edu/music21/)

## 🤝 Contribuindo

Sinta-se à vontade para:
- Adicionar novos estilos musicais
- Melhorar a qualidade dos samples
- Implementar novos efeitos
- Corrigir bugs

## 📄 Licença

Este projeto é open source e está disponível para uso educacional e pessoal.

## 💡 Dicas

1. **Use uma DAW** como Ableton Live ou FL Studio para refinar suas músicas
2. **Importe os MIDIs** gerados em sua DAW favorita para mais controle
3. **Aplique plugins VST** para efeitos profissionais (autotune, compressão, EQ)
4. **Experimente!** Mude BPMs, padrões, notas e crie seu próprio estilo

---

**Criado com ❤️ e Python** 🐍🎵
