"""
Exemplo Rápido - Quick Start
Execute este arquivo para testar tudo rapidamente
"""

import sys
import os

# Definir diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
SAMPLES_DIR = os.path.join(BASE_DIR, 'samples')

# Adicionar diretório src ao path
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from beat_generator import BeatGenerator
from voice_generator import VoiceGenerator
from music_composer import MusicComposer


def quick_demo():
    """Demo rápido de todas as funcionalidades"""
    
    print("=" * 70)
    print(" 🎵 MUSIC GENERATOR - DEMO RÁPIDO")
    print("=" * 70)
    print("\nEste demo vai criar:")
    print("  1. Uma batida de funk (MIDI + samples)")
    print("  2. Uma voz sintetizada")
    print("  3. Uma música completa de 20 segundos\n")
    
    input("Pressione ENTER para começar...")
    
    # 1. Criar batida
    print("\n" + "-" * 70)
    print("PASSO 1: Gerando batida de FUNK")
    print("-" * 70)
    
    beat = BeatGenerator(tempo=128)
    beat.create_funk_pattern(bars=4)
    beat.add_bassline(pattern='funk', bars=4)
    beat.save_midi(os.path.join(OUTPUT_DIR, 'demo_beat.mid'))
    
    # Gerar samples
    kick = BeatGenerator.create_808_kick()
    kick.export(os.path.join(SAMPLES_DIR, 'demo_kick.wav'), format='wav')
    print("✓ Samples gerados")
    
    # 2. Criar voz
    print("\n" + "-" * 70)
    print("PASSO 2: Gerando voz")
    print("-" * 70)
    
    vg = VoiceGenerator()
    vg.text_to_speech(
        "Ai Alê!!! Mete com força, mete! David vai com força! Ai ai ai!",
        language='pt-br',
        filename=os.path.join(OUTPUT_DIR, 'demo_voice.mp3')
    )
    
    # 3. Criar música completa
    print("\n" + "-" * 70)
    print("PASSO 3: Compondo música completa")
    print("-" * 70)
    
    composer = MusicComposer(tempo=128)
    
    # Configurar caminhos corretos
    composer.output_dir = OUTPUT_DIR
    composer.samples_dir = SAMPLES_DIR
    
    # Criar faixa base
    track = composer.build_audio_track(style='funk', duration_seconds=20)
    
    # Adicionar melodia
    notes = [60, 62, 64, 65, 67, 65, 64, 62, 60] * 2
    durations = [300, 300, 300, 300, 400, 300, 300, 300, 600] * 2
    
    track_with_melody = composer.add_melody(
        track,
        notes,
        durations,
        start_time=1000
    )
    
    # Exportar
    output_file = os.path.join(OUTPUT_DIR, 'demo_song.mp3')
    track_with_melody.normalize().export(output_file, format='mp3', bitrate='320k')
    print(f"\n✅ Faixa exportada: {output_file}")
    
    # Resultado
    print("\n" + "=" * 70)
    print(" ✅ DEMO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print("\n📁 Arquivos criados em 'output/':")
    print("   • demo_beat.mid - Batida em MIDI")
    print("   • demo_voice.mp3 - Voz sintetizada")
    print("   • demo_song.mp3 - Música completa (20s)")
    print("\n💡 Próximos passos:")
    print("   1. Execute os scripts individuais para mais opções")
    print("   2. Edite o código para personalizar")
    print("   3. Importe os arquivos em uma DAW para refinar")
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        quick_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo cancelado pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro: {e}")
        print("\n💡 Certifique-se de ter instalado as dependências:")
        print("   pip install -r requirements.txt")
        print("\n   E também o FFmpeg (necessário para pydub)")
