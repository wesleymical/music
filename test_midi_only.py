"""
Teste rápido - Apenas MIDI (sem precisar de FFmpeg)
Execute este para testar sem dependência de áudio
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from beat_generator import BeatGenerator


def test_midi_only():
    """Testa apenas geração MIDI (não precisa de FFmpeg)"""
    
    print("=" * 70)
    print(" 🎵 TESTE RÁPIDO - Apenas MIDI")
    print("=" * 70)
    print("\nGerando batidas em formato MIDI...")
    print("(MIDI não precisa de FFmpeg - pode abrir em qualquer DAW)\n")
    
    # Gerar batida de Funk
    print("1. Criando batida FUNK...")
    funk_beat = BeatGenerator(tempo=128)
    funk_beat.create_funk_pattern(bars=8)
    funk_beat.add_bassline(pattern='funk', bars=8)
    funk_beat.save_midi("output/funk_beat_teste.mid")
    
    # Gerar batida Pop
    print("2. Criando batida POP...")
    pop_beat = BeatGenerator(tempo=120)
    pop_beat.create_pop_pattern(bars=8)
    pop_beat.add_bassline(pattern='pop', bars=8)
    pop_beat.save_midi("output/pop_beat_teste.mid")
    
    print("\n" + "=" * 70)
    print(" ✅ SUCESSO!")
    print("=" * 70)
    print("\n📁 Arquivos MIDI criados em 'output/':")
    print("   • funk_beat_teste.mid")
    print("   • pop_beat_teste.mid")
    print("\n💡 Como usar:")
    print("   1. Abra esses arquivos em:")
    print("      - FL Studio, Ableton, Logic Pro, GarageBand")
    print("      - Online: https://signal.vercel.app/edit")
    print("      - MuseScore (notação musical)")
    print("   2. Escolha seus próprios instrumentos/samples")
    print("   3. Produza sua música!")
    print("\n   Depois de instalar FFmpeg corretamente, você poderá")
    print("   gerar áudio e vozes também!")
    print("=" * 70)
    print()


if __name__ == "__main__":
    try:
        test_midi_only()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\nVerifique se instalou as dependências:")
        print("   pip install -r requirements.txt")
