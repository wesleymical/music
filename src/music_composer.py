"""
Music Composer - Compositor Musical Completo
Combina batidas, vozes e efeitos para criar músicas completas
"""

from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pydub.playback import play
import os
from beat_generator import BeatGenerator
from voice_generator import VoiceGenerator


class MusicComposer:
    def __init__(self, tempo=120):
        self.tempo = tempo
        self.beat_gen = BeatGenerator(tempo=tempo)
        self.voice_gen = VoiceGenerator()
        self.tracks = {}
        
        # Definir diretórios base
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.samples_dir = os.path.join(self.base_dir, 'samples')
    
    def create_complete_track(self, style='funk', bars=16):
        """
        Cria uma faixa completa com batida, baixo e estrutura
        
        Args:
            style: 'funk' ou 'pop'
            bars: Número de compassos
        """
        print(f"\n🎵 Criando faixa {style.upper()} ({bars} compassos)...\n")
        
        # Gerar batida MIDI
        if style == 'funk':
            self.beat_gen.create_funk_pattern(bars=bars)
            self.beat_gen.add_bassline(pattern='funk', bars=bars)
        else:
            self.beat_gen.create_pop_pattern(bars=bars)
            self.beat_gen.add_bassline(pattern='pop', bars=bars)
        
        # Salvar MIDI
        midi_file = os.path.join(self.output_dir, f'{style}_track.mid')
        self.beat_gen.save_midi(midi_file)
        
        return midi_file
    
    def build_audio_track(self, style='funk', duration_seconds=30):
        """
        Constrói faixa de áudio completa com samples
        
        Args:
            style: 'funk' ou 'pop'
            duration_seconds: Duração total em segundos
        """
        print(f"\n🎶 Construindo faixa de áudio {style}...\n")
        
        # Criar samples sintéticos se não existirem
        self._ensure_samples()
        
        # Carregar samples
        kick = AudioSegment.from_wav(os.path.join(self.samples_dir, "kick_808.wav"))
        snare = AudioSegment.from_wav(os.path.join(self.samples_dir, "snare.wav"))
        hihat = AudioSegment.from_wav(os.path.join(self.samples_dir, "hihat.wav"))
        
        # Calcular timing baseado no BPM
        beat_duration = 60000 / self.tempo  # ms por beat
        
        # Criar faixa vazia
        track = AudioSegment.silent(duration=duration_seconds * 1000)
        
        # Padrões rítmicos
        if style == 'funk':
            kick_pattern = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]  # Beats na barra
            snare_pattern = [1, 3]
            hihat_pattern = [i/4 for i in range(16)]  # 16th notes
        else:  # pop
            kick_pattern = [0, 1, 2, 3]
            snare_pattern = [1, 3]
            hihat_pattern = [i/2 for i in range(8)]  # 8th notes
        
        # Construir batida loop
        bars = int((duration_seconds * 1000) / (beat_duration * 4)) + 1
        
        for bar in range(bars):
            bar_start = bar * beat_duration * 4
            
            # Adicionar kicks
            for beat in kick_pattern:
                position = int(bar_start + beat * beat_duration)
                if position < len(track):
                    track = track.overlay(kick, position=position)
            
            # Adicionar snares
            for beat in snare_pattern:
                position = int(bar_start + beat * beat_duration)
                if position < len(track):
                    track = track.overlay(snare, position=position)
            
            # Adicionar hi-hats
            for beat in hihat_pattern:
                position = int(bar_start + beat * beat_duration)
                if position < len(track):
                    velocity = 0.8 if int(beat * 4) % 2 == 0 else 0.5
                    hat = hihat - (20 * (1 - velocity))  # Variar volume
                    track = track.overlay(hat, position=position)
        
        # Normalizar e comprimir
        track = normalize(track)
        track = compress_dynamic_range(track)
        
        return track
    
    def add_vocals(self, track, lyrics, start_time=4000):
        """
        Adiciona vocais à faixa
        
        Args:
            track: AudioSegment da faixa base
            lyrics: Texto ou arquivo de vocal
            start_time: Quando começar o vocal (ms)
        """
        print("\n🎤 Adicionando vocais...")
        
        # Se lyrics for texto, gerar TTS
        if isinstance(lyrics, str) and not os.path.exists(lyrics):
            vocal_file = os.path.join(self.output_dir, 'temp_vocal.mp3')
            self.voice_gen.text_to_speech(lyrics, filename=vocal_file)
        else:
            vocal_file = lyrics
        
        # Carregar vocal
        vocal = AudioSegment.from_file(vocal_file)
        
        # Processar vocal (normalizar, EQ básico)
        vocal = normalize(vocal)
        
        # Adicionar reverb simples (simulado com eco)
        vocal_with_fx = vocal
        echo = vocal - 12  # -12dB
        vocal_with_fx = vocal_with_fx.overlay(echo, position=100)  # 100ms delay
        
        # Mixar com a faixa
        result = track.overlay(vocal_with_fx, position=start_time)
        
        # Limpar temp
        if 'temp_vocal' in vocal_file and os.path.exists(vocal_file):
            os.remove(vocal_file)
        
        print("✓ Vocais adicionados")
        return result
    
    def add_melody(self, track, notes, durations, start_time=0, instrument='synth'):
        """
        Adiciona melodia à faixa
        
        Args:
            track: AudioSegment da faixa base
            notes: Lista de notas MIDI
            durations: Lista de durações (ms)
            start_time: Quando começar (ms)
            instrument: Tipo de som (não implementado totalmente)
        """
        print(f"\n🎹 Adicionando melodia ({instrument})...")
        
        # Criar melodia
        melody_file = os.path.join(self.output_dir, 'temp_melody.wav')
        self.voice_gen.create_vocal_melody(notes, durations, melody_file)
        
        # Carregar e processar
        melody = AudioSegment.from_wav(melody_file)
        melody = melody - 6  # Reduzir volume para mixagem
        
        # Adicionar à faixa
        result = track.overlay(melody, position=start_time)
        
        # Limpar
        if os.path.exists(melody_file):
            os.remove(melody_file)
        
        print("✓ Melodia adicionada")
        return result
    
    def create_song_structure(self, style='pop'):
        """
        Cria estrutura completa de música (intro, verse, chorus, etc.)
        """
        print(f"\n🎼 Criando estrutura completa de música {style}...\n")
        
        # Definir seções (em segundos)
        sections = {
            'intro': 8,
            'verse1': 16,
            'chorus': 16,
            'verse2': 16,
            'chorus2': 16,
            'outro': 8
        }
        
        song = AudioSegment.empty()
        
        for section_name, duration in sections.items():
            print(f"  • Construindo {section_name}...")
            
            # Criar seção
            section = self.build_audio_track(style=style, duration_seconds=duration)
            
            # Aplicar efeitos específicos por seção
            if 'intro' in section_name:
                section = section.fade_in(2000)
            elif 'outro' in section_name:
                section = section.fade_out(3000)
            elif 'chorus' in section_name:
                # Chorus mais alto
                section = section + 2
            
            song += section
        
        print("\n✓ Estrutura criada")
        return song
    
    def export_track(self, track, filename, format='mp3'):
        """Exporta a faixa final"""
        # Normalização final
        track = normalize(track)
        
        # Exportar
        output_path = os.path.join(self.output_dir, f'{filename}.{format}')
        track.export(output_path, format=format, bitrate='320k')
        print(f"\n✅ Faixa exportada: {output_path}")
        return output_path
    
    def _ensure_samples(self):
        """Garante que os samples existam"""
        samples_needed = {
            'kick_808.wav': 'kick',
            'snare.wav': 'snare',
            'hihat.wav': 'hihat'
        }
        
        for filename, sample_type in samples_needed.items():
            sample_path = os.path.join(self.samples_dir, filename)
            if not os.path.exists(sample_path):
                print(f"Gerando sample: {sample_path}")
                if sample_type == 'kick':
                    self.beat_gen.create_808_kick().export(sample_path, format='wav')
                elif sample_type == 'snare':
                    self.beat_gen.create_snare().export(sample_path, format='wav')
                elif sample_type == 'hihat':
                    self.beat_gen.create_hihat().export(sample_path, format='wav')


def main():
    """Exemplo completo de composição"""
    print("=" * 60)
    print("🎵 MUSIC COMPOSER - Criador de Músicas Completas")
    print("=" * 60)
    
    # Criar compositor
    composer = MusicComposer(tempo=128)
    
    # Exemplo 1: Faixa FUNK simples
    print("\n" + "=" * 60)
    print("EXEMPLO 1: FAIXA FUNK")
    print("=" * 60)
    
    funk_track = composer.build_audio_track(style='funk', duration_seconds=20)
    
    # Adicionar melodia funk
    funk_notes = [60, 62, 64, 62, 60, 59, 60, 60] * 2
    funk_durations = [300, 300, 300, 300, 400, 200, 200, 400] * 2
    
    funk_with_melody = composer.add_melody(
        funk_track,
        funk_notes,
        funk_durations,
        start_time=2000
    )
    
    composer.export_track(funk_with_melody, 'funk_complete', format='mp3')
    
    # Exemplo 2: Faixa POP com vocais
    print("\n" + "=" * 60)
    print("EXEMPLO 2: FAIXA POP COM VOCAIS")
    print("=" * 60)
    
    pop_track = composer.build_audio_track(style='pop', duration_seconds=20)
    
    # Adicionar vocais
    lyrics = "This is the future, digital music creation"
    pop_with_vocals = composer.add_vocals(
        pop_track,
        lyrics,
        start_time=4000
    )
    
    # Adicionar melodia pop
    pop_notes = [64, 64, 65, 67, 65, 64, 62, 60, 62, 64, 64, 62]
    pop_durations = [400, 400, 400, 600, 200, 400, 400, 400, 400, 400, 800, 800]
    
    pop_complete = composer.add_melody(
        pop_with_vocals,
        pop_notes,
        pop_durations,
        start_time=0
    )
    
    composer.export_track(pop_complete, 'pop_complete', format='mp3')
    
    # Exemplo 3: Música completa estruturada
    print("\n" + "=" * 60)
    print("EXEMPLO 3: MÚSICA COMPLETA (ESTRUTURADA)")
    print("=" * 60)
    
    full_song = composer.create_song_structure(style='pop')
    composer.export_track(full_song, 'full_song_structured', format='mp3')
    
    print("\n" + "=" * 60)
    print("✨ TODAS AS FAIXAS FORAM GERADAS COM SUCESSO!")
    print("=" * 60)
    print("\n📁 Arquivos gerados na pasta 'output':")
    print("   • funk_complete.mp3")
    print("   • pop_complete.mp3")
    print("   • full_song_structured.mp3")
    print("\n💡 Dica: Importe essas faixas em uma DAW (Ableton, FL Studio)")
    print("   para adicionar mais efeitos e refinamento!")
    print("=" * 60)


if __name__ == "__main__":
    main()
