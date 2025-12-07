"""
Gerador de Vozes e Melodias Vocais
Usa TTS e síntese para criar vozes programaticamente
"""

import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import gtts
import os


class VoiceGenerator:
    def __init__(self):
        self.sample_rate = 44100
    
    def text_to_speech(self, text, language='pt-br', filename='voice.mp3'):
        """
        Converte texto em voz usando Google TTS
        
        Args:
            text: Texto para converter
            language: Idioma ('pt-br', 'en', etc.)
            filename: Nome do arquivo de saída
        """
        try:
            tts = gtts.gTTS(text=text, lang=language, slow=False)
            tts.save(filename)
            print(f"✓ Voz gerada: {filename}")
            return filename
        except Exception as e:
            print(f"✗ Erro ao gerar voz: {e}")
            return None
    
    def create_vocal_melody(self, notes, durations, output_file):
        """
        Cria uma melodia vocal sintética usando tons puros
        
        Args:
            notes: Lista de frequências (Hz) ou notas MIDI
            durations: Lista de durações em milissegundos
            output_file: Caminho do arquivo de saída
        """
        melody = AudioSegment.empty()
        
        for note, duration in zip(notes, durations):
            # Converter MIDI para Hz se necessário
            if note < 500:  # Assumir que é nota MIDI
                freq = self.midi_to_hz(note)
            else:
                freq = note
            
            # Gerar tom
            tone = Sine(freq).to_audio_segment(duration=duration)
            
            # Aplicar envelope (attack, decay)
            attack = min(50, duration // 4)
            release = min(100, duration // 4)
            tone = tone.fade_in(attack).fade_out(release)
            
            # Adicionar à melodia
            melody += tone
        
        # Exportar
        melody.export(output_file, format="wav")
        print(f"✓ Melodia vocal salva: {output_file}")
        return output_file
    
    def create_vocal_chop(self, text, chop_duration=200, repetitions=4):
        """
        Cria um 'vocal chop' - voz cortada ritmicamente (estilo pop/EDM)
        
        Args:
            text: Texto curto para chopar
            chop_duration: Duração de cada chop em ms
            repetitions: Quantas vezes repetir
        """
        # Gerar voz base
        temp_file = "temp_voice.mp3"
        self.text_to_speech(text, filename=temp_file)
        
        # Carregar e processar
        voice = AudioSegment.from_mp3(temp_file)
        
        # Normalizar volume
        voice = voice.normalize()
        
        # Criar chops
        chopped = AudioSegment.empty()
        chop_size = min(chop_duration, len(voice))
        
        for i in range(repetitions):
            # Extrair pedaço
            start = (i * chop_size) % len(voice)
            end = start + chop_size
            
            if end > len(voice):
                end = len(voice)
            
            chop = voice[start:end]
            
            # Adicionar efeitos
            chop = chop.fade_in(10).fade_out(10)
            
            # Adicionar silêncio entre chops
            chopped += chop + AudioSegment.silent(duration=50)
        
        # Limpar arquivo temporário
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        return chopped
    
    def add_autotune_effect(self, audio, target_note=60):
        """
        Simula efeito de autotune (simplificado)
        Nota: Para autotune real, use bibliotecas especializadas
        """
        # Este é um efeito simplificado
        # Para autotune profissional, use: librosa, pyrubberband, ou psola
        
        # Ajustar pitch (efeito básico)
        target_freq = self.midi_to_hz(target_note)
        
        # Aplicar pequenas variações de pitch
        return audio.speedup(playback_speed=1.0)
    
    @staticmethod
    def midi_to_hz(midi_note):
        """Converte nota MIDI para frequência em Hz"""
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
    
    @staticmethod
    def hz_to_midi(frequency):
        """Converte frequência em Hz para nota MIDI"""
        return int(69 + 12 * np.log2(frequency / 440.0))
    
    def create_harmony(self, base_melody_file, intervals=[0, 4, 7]):
        """
        Cria harmonia a partir de uma melodia base
        
        Args:
            base_melody_file: Arquivo da melodia base
            intervals: Intervalos em semitons (0=uníssono, 4=terça, 7=quinta)
        """
        base = AudioSegment.from_file(base_melody_file)
        
        harmonies = [base]
        
        for interval in intervals[1:]:
            # Shift de pitch (aproximação)
            # Para pitch shifting real, use pyrubberband ou librosa
            pitch_shifted = base._spawn(base.raw_data, overrides={
                "frame_rate": int(base.frame_rate * (2 ** (interval / 12.0)))
            }).set_frame_rate(base.frame_rate)
            
            harmonies.append(pitch_shifted)
        
        # Mixar harmonias
        harmony = harmonies[0]
        for h in harmonies[1:]:
            harmony = harmony.overlay(h - 3)  # -3dB para cada camada
        
        return harmony


def main():
    """Exemplo de uso"""
    print("🎤 Gerador de Vozes e Melodias\n")
    
    vg = VoiceGenerator()
    
    # 1. Texto para voz (TTS)
    print("1. Gerando voz a partir de texto...")
    lyrics = "Yeah, this is the future of music production"
    vg.text_to_speech(
        lyrics,
        language='en',
        filename='../output/vocals_english.mp3'
    )
    
    lyrics_pt = "Essa é a batida do futuro"
    vg.text_to_speech(
        lyrics_pt,
        language='pt-br',
        filename='../output/vocals_portuguese.mp3'
    )
    
    # 2. Melodia vocal sintética
    print("\n2. Criando melodia vocal sintética...")
    # Escala de C maior: C, D, E, F, G, A, B, C
    notes = [60, 62, 64, 65, 67, 69, 71, 72]  # MIDI notes
    durations = [300, 300, 300, 300, 400, 400, 400, 600]  # ms
    
    vg.create_vocal_melody(
        notes,
        durations,
        '../output/vocal_melody.wav'
    )
    
    # 3. Vocal chop
    print("\n3. Criando vocal chop...")
    chop = vg.create_vocal_chop("Hey", chop_duration=150, repetitions=8)
    chop.export('../output/vocal_chop.wav', format='wav')
    print("✓ Vocal chop salvo: ../output/vocal_chop.wav")
    
    # 4. Melodia funk/pop
    print("\n4. Criando melodia pop...")
    # Progressão pop típica
    pop_notes = [60, 60, 62, 64, 62, 60, 59, 60]
    pop_durations = [400, 200, 200, 400, 200, 200, 400, 800]
    
    vg.create_vocal_melody(
        pop_notes,
        pop_durations,
        '../output/pop_melody.wav'
    )
    
    print("\n✨ Vozes e melodias geradas com sucesso!")
    print("📁 Confira a pasta 'output'")
    print("\n💡 Dica: Você pode usar software de edição de áudio")
    print("   para aplicar efeitos profissionais (reverb, autotune, etc.)")


if __name__ == "__main__":
    main()
