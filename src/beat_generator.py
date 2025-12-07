"""
Gerador de Batidas de Funk e Pop
Cria beats programaticamente usando MIDI e síntese de áudio
"""

from midiutil import MIDIFile
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine, Square, WhiteNoise
import random


class BeatGenerator:
    def __init__(self, tempo=120):
        self.tempo = tempo
        self.midi = MIDIFile(4)  # 4 tracks: kick, snare, hihat, bass
        
        # Configurar tracks
        self.track_kick = 0
        self.track_snare = 1
        self.track_hihat = 2
        self.track_bass = 3
        
        for track in range(4):
            self.midi.addTempo(track, 0, tempo)
    
    def create_funk_pattern(self, bars=4):
        """Cria um padrão de funk brasileiro"""
        beats_per_bar = 16  # 16th notes
        
        for bar in range(bars):
            base_time = bar * 4  # 4 beats por barra
            
            # Kick pattern (funk carioca style)
            kick_pattern = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
            for beat in kick_pattern:
                self.midi.addNote(self.track_kick, 0, 36, base_time + beat, 0.25, 100)
            
            # Snare (backbeat)
            snare_pattern = [1, 3]
            for beat in snare_pattern:
                self.midi.addNote(self.track_snare, 0, 38, base_time + beat, 0.25, 90)
            
            # Hi-hat (padrão acelerado)
            for i in range(16):
                velocity = 80 if i % 2 == 0 else 60
                self.midi.addNote(self.track_hihat, 0, 42, base_time + i/4, 0.125, velocity)
    
    def create_pop_pattern(self, bars=4):
        """Cria um padrão pop moderno"""
        for bar in range(bars):
            base_time = bar * 4
            
            # Kick (four on the floor com variações)
            kick_pattern = [0, 1, 2, 3]
            for beat in kick_pattern:
                self.midi.addNote(self.track_kick, 0, 36, base_time + beat, 0.5, 100)
            
            # Snare/Clap (backbeat)
            self.midi.addNote(self.track_snare, 0, 38, base_time + 1, 0.25, 95)
            self.midi.addNote(self.track_snare, 0, 38, base_time + 3, 0.25, 95)
            
            # Hi-hat (8th notes)
            for i in range(8):
                velocity = 85 if i % 2 == 0 else 65
                self.midi.addNote(self.track_hihat, 0, 42, base_time + i/2, 0.25, velocity)
    
    def add_bassline(self, pattern='funk', bars=4):
        """Adiciona linha de baixo"""
        notes = {
            'funk': [36, 36, 38, 36, 36, 38, 36, 38],  # C, C, D, C pattern
            'pop': [36, 43, 36, 43, 38, 43, 38, 43]     # C, G, C, G, D, G pattern
        }
        
        bass_notes = notes.get(pattern, notes['funk'])
        
        for bar in range(bars):
            for i, note in enumerate(bass_notes):
                time = bar * 4 + i/2
                self.midi.addNote(self.track_bass, 0, note, time, 0.4, 80)
    
    def save_midi(self, filename):
        """Salva o MIDI gerado"""
        with open(filename, "wb") as output_file:
            self.midi.writeFile(output_file)
        print(f"✓ MIDI salvo: {filename}")
    
    @staticmethod
    def create_808_kick():
        """Cria um kick 808 sintético"""
        duration = 500  # ms
        
        # Fundamental (baixa frequência com pitch envelope)
        t = np.linspace(0, duration/1000, int(44100 * duration/1000))
        freq_envelope = 60 * np.exp(-8 * t)  # Pitch decay
        phase = 2 * np.pi * np.cumsum(freq_envelope) / 44100
        kick = np.sin(phase)
        
        # Amplitude envelope
        amp_envelope = np.exp(-5 * t)
        kick = kick * amp_envelope
        
        # Converter para AudioSegment
        kick_normalized = np.int16(kick * 32767)
        kick_audio = AudioSegment(
            kick_normalized.tobytes(),
            frame_rate=44100,
            sample_width=2,
            channels=1
        )
        return kick_audio
    
    @staticmethod
    def create_snare():
        """Cria um snare sintético"""
        duration = 200
        
        # Tom (componente tonal)
        tone = Sine(200).to_audio_segment(duration=duration)
        
        # Ruído (componente de ruído)
        noise_samples = np.random.uniform(-1, 1, int(44100 * duration/1000))
        noise_normalized = np.int16(noise_samples * 32767 * 0.3)
        noise = AudioSegment(
            noise_normalized.tobytes(),
            frame_rate=44100,
            sample_width=2,
            channels=1
        )
        
        # Mixar
        snare = tone.overlay(noise)
        
        # Fade out rápido
        return snare.fade_out(150)
    
    @staticmethod
    def create_hihat():
        """Cria um hi-hat sintético"""
        duration = 50
        
        # Ruído filtrado (high-pass)
        noise_samples = np.random.uniform(-1, 1, int(44100 * duration/1000))
        noise_normalized = np.int16(noise_samples * 32767 * 0.15)
        hihat = AudioSegment(
            noise_normalized.tobytes(),
            frame_rate=44100,
            sample_width=2,
            channels=1
        )
        
        return hihat.fade_out(30)


def main():
    """Exemplo de uso"""
    print("🎵 Gerador de Batidas - Funk & Pop\n")
    
    # Gerar batida de Funk
    print("Gerando batida de FUNK...")
    funk_beat = BeatGenerator(tempo=128)
    funk_beat.create_funk_pattern(bars=8)
    funk_beat.add_bassline(pattern='funk', bars=8)
    funk_beat.save_midi("../output/funk_beat.mid")
    
    # Gerar batida Pop
    print("Gerando batida de POP...")
    pop_beat = BeatGenerator(tempo=120)
    pop_beat.create_pop_pattern(bars=8)
    pop_beat.add_bassline(pattern='pop', bars=8)
    pop_beat.save_midi("../output/pop_beat.mid")
    
    # Gerar samples sintéticos
    print("\nGerando samples sintéticos...")
    kick = BeatGenerator.create_808_kick()
    kick.export("../samples/kick_808.wav", format="wav")
    print("✓ Kick 808 salvo")
    
    snare = BeatGenerator.create_snare()
    snare.export("../samples/snare.wav", format="wav")
    print("✓ Snare salvo")
    
    hihat = BeatGenerator.create_hihat()
    hihat.export("../samples/hihat.wav", format="wav")
    print("✓ Hi-hat salvo")
    
    print("\n✨ Batidas geradas com sucesso!")
    print("📁 Confira a pasta 'output' e 'samples'")


if __name__ == "__main__":
    main()
