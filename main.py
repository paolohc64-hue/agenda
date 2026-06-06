#!/usr/bin/env python3
"""
Sistema di Gestione Agenda Completa
Applicazione per gestire e visualizzare parametri di privati e aziende
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class AgendaManager:
    """Gestore principale dell'agenda completa"""
    
    def __init__(self, config_file: str = "agenda_parametri.json"):
        """
        Inizializza il gestore dell'agenda
        
        Args:
            config_file: Percorso del file JSON dell'agenda
        """
        self.config_file = config_file
        self.agenda: Dict[str, Any] = {}
        self.carica_agenda()
    
    def carica_agenda(self) -> None:
        """Carica il file JSON dell'agenda"""
        try:
            if not os.path.exists(self.config_file):
                print(f"❌ Errore: File '{self.config_file}' non trovato")
                sys.exit(1)
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.agenda = json.load(f)
            print(f"✅ Agenda caricata con successo da '{self.config_file}'")
        except json.JSONDecodeError as e:
            print(f"❌ Errore nel parsing JSON: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Errore durante il caricamento: {e}")
            sys.exit(1)
    
    def salva_agenda(self) -> None:
        """Salva l'agenda corrente nel file JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.agenda, f, indent=2, ensure_ascii=False)
            print(f"✅ Agenda salvata con successo in '{self.config_file}'")
        except Exception as e:
            print(f"❌ Errore durante il salvataggio: {e}")
    
    def visualizza_menu(self) -> None:
        """Visualizza il menu principale"""
        print("\n" + "="*60)
        print("📋 SISTEMA DI GESTIONE AGENDA COMPLETA")
        print("="*60)
        print("\n🔍 OPZIONI DISPONIBILI:\n")
        print("1️⃣  Visualizza Parametri Personali")
        print("2️⃣  Visualizza Parametri Aziendali")
        print("3️⃣  Visualizza Parametri Fiscali/Contabili")
        print("4️⃣  Visualizza Parametri Bancari/Finanziari")
        print("5️⃣  Visualizza Parametri Legali/Contrattuali")
        print("6️⃣  Visualizza Parametri Sicurezza/Privacy")
        print("7️⃣  Modifica Parametri")
        print("8️⃣  Cerca Parametro")
        print("9️⃣  Esporta Agenda (JSON)")
        print("🔟 Importa Agenda (JSON)")
        print("1️⃣1️⃣ Genera Report")
        print("1️⃣2️⃣ Esci")
        print("\n" + "-"*60)
    
    def visualizza_sezione(self, sezione: str) -> None:
        """
        Visualizza una sezione dell'agenda
        
        Args:
            sezione: Nome della sezione da visualizzare
        """
        if "agenda_completa" not in self.agenda:
            print("❌ Errore: Struttura agenda non valida")
            return
        
        agenda_data = self.agenda["agenda_completa"]
        
        if sezione not in agenda_data:
            print(f"❌ Sezione '{sezione}' non trovata")
            return
        
        dati = agenda_data[sezione]
        print(f"\n📄 {self._formatta_nome_sezione(sezione)}")
        print("="*60)
        self._stampa_ricorsivo(dati, indentazione=0)
    
    def _stampa_ricorsivo(self, obj: Any, indentazione: int = 0) -> None:
        """
        Stampa ricorsivamente un oggetto JSON formattato
        
        Args:
            obj: Oggetto da stampare
            indentazione: Livello di indentazione
        """
        indent = "  " * indentazione
        
        if isinstance(obj, dict):
            for chiave, valore in obj.items():
                chiave_formattata = chiave.replace("_", " ").title()
                if isinstance(valore, (dict, list)):
                    print(f"{indent}📌 {chiave_formattata}:")
                    self._stampa_ricorsivo(valore, indentazione + 1)
                else:
                    valore_str = str(valore) if valore else "[Vuoto]"
                    print(f"{indent}   {chiave_formattata}: {valore_str}")
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj, 1):
                if isinstance(item, dict):
                    print(f"{indent}📍 Elemento {i}:")
                    self._stampa_ricorsivo(item, indentazione + 1)
                else:
                    print(f"{indent}  - {item}")
    
    def modifica_parametro(self) -> None:
        """Interfaccia per modificare parametri"""
        print("\n" + "="*60)
        print("✏️  MODIFICA PARAMETRI")
        print("="*60)
        
        print("\nSezioni disponibili:")
        sezioni = list(self.agenda.get("agenda_completa", {}).keys())
        for i, sezione in enumerate(sezioni, 1):
            print(f"{i}. {self._formatta_nome_sezione(sezione)}")
        
        try:
            scelta = int(input("\nSeleziona sezione (numero): ")) - 1
            if 0 <= scelta < len(sezioni):
                sezione = sezioni[scelta]
                self._modifica_sezione(sezione)
            else:
                print("❌ Scelta non valida")
        except ValueError:
            print("❌ Inserisci un numero valido")
    
    def _modifica_sezione(self, sezione: str) -> None:
        """Modifica una sezione specifica"""
        percorso = input(f"\nInserisci il percorso del parametro (es: dati_anagrafici.nome): ")
        nuovo_valore = input("Inserisci il nuovo valore: ")
        
        try:
            chiavi = percorso.split(".")
            obj = self.agenda["agenda_completa"][sezione]
            
            for chiave in chiavi[:-1]:
                obj = obj[chiave]
            
            obj[chiavi[-1]] = nuovo_valore
            print(f"✅ Parametro aggiornato con successo")
            self.salva_agenda()
        except (KeyError, IndexError, TypeError) as e:
            print(f"❌ Errore nell'accesso al parametro: {e}")
    
    def cerca_parametro(self) -> None:
        """Ricerca un parametro nell'agenda"""
        print("\n" + "="*60)
        print("🔍 RICERCA PARAMETRO")
        print("="*60)
        
        ricerca = input("\nInserisci la chiave da cercare: ").lower()
        risultati = self._ricerca_ricorsiva(self.agenda, ricerca)
        
        if risultati:
            print(f"\n✅ Trovati {len(risultati)} risultati:\n")
            for percorso, valore in risultati:
                print(f"📍 {percorso}: {valore}")
        else:
            print("❌ Nessun risultato trovato")
    
    def _ricerca_ricorsiva(self, obj: Any, chiave: str, percorso: str = "") -> List[tuple]:
        """
        Ricerca ricorsiva di una chiave nell'oggetto
        
        Args:
            obj: Oggetto da cercare
            chiave: Chiave da cercare
            percorso: Percorso attuale
        
        Returns:
            Lista di tuple (percorso, valore)
        """
        risultati = []
        
        if isinstance(obj, dict):
            for k, v in obj.items():
                nuovo_percorso = f"{percorso}.{k}" if percorso else k
                
                if chiave in k.lower():
                    risultati.append((nuovo_percorso, v))
                
                risultati.extend(self._ricerca_ricorsiva(v, chiave, nuovo_percorso))
        
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                nuovo_percorso = f"{percorso}[{i}]"
                risultati.extend(self._ricerca_ricorsiva(item, chiave, nuovo_percorso))
        
        return risultati
    
    def esporta_agenda(self) -> None:
        """Esporta l'agenda in un file JSON"""
        nome_file = input("\nInserisci il nome del file di export (senza estensione): ")
        nome_file = f"{nome_file}.json"
        
        try:
            with open(nome_file, 'w', encoding='utf-8') as f:
                json.dump(self.agenda, f, indent=2, ensure_ascii=False)
            print(f"✅ Agenda esportata con successo in '{nome_file}'")
        except Exception as e:
            print(f"❌ Errore durante l'export: {e}")
    
    def importa_agenda(self) -> None:
        """Importa un'agenda da un file JSON"""
        nome_file = input("\nInserisci il percorso del file JSON da importare: ")
        
        try:
            with open(nome_file, 'r', encoding='utf-8') as f:
                nuova_agenda = json.load(f)
            
            self.agenda = nuova_agenda
            self.salva_agenda()
            print(f"✅ Agenda importata con successo da '{nome_file}'")
        except FileNotFoundError:
            print(f"❌ File '{nome_file}' non trovato")
        except json.JSONDecodeError:
            print(f"❌ Il file non è un JSON valido")
        except Exception as e:
            print(f"❌ Errore durante l'import: {e}")
    
    def genera_report(self) -> None:
        """Genera un report completo dell'agenda"""
        print("\n" + "="*60)
        print("📊 GENERAZIONE REPORT")
        print("="*60)
        
        nome_file = input("\nInserisci il nome del file di report (senza estensione): ")
        nome_file = f"{nome_file}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(nome_file, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("REPORT AGENDA COMPLETA\n")
                f.write("="*60 + "\n")
                f.write(f"Generato il: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                agenda_data = self.agenda.get("agenda_completa", {})
                for sezione, dati in agenda_data.items():
                    f.write(f"\n{'='*60}\n")
                    f.write(f"{self._formatta_nome_sezione(sezione)}\n")
                    f.write(f"{'='*60}\n")
                    f.write(json.dumps(dati, indent=2, ensure_ascii=False))
                    f.write("\n")
            
            print(f"✅ Report generato con successo: '{nome_file}'")
        except Exception as e:
            print(f"❌ Errore durante la generazione del report: {e}")
    
    @staticmethod
    def _formatta_nome_sezione(nome: str) -> str:
        """Formatta il nome di una sezione"""
        emojis = {
            "parametri_personali": "👤 Parametri Personali",
            "parametri_aziendali": "🏢 Parametri Aziendali",
            "parametri_fiscali_contabili": "📊 Parametri Fiscali/Contabili",
            "parametri_bancari_finanziari": "🏦 Parametri Bancari/Finanziari",
            "parametri_legali_contrattuali": "⚖️ Parametri Legali/Contrattuali",
            "parametri_sicurezza_privacy": "🔒 Parametri Sicurezza/Privacy"
        }
        return emojis.get(nome, nome.replace("_", " ").title())
    
    def esegui(self) -> None:
        """Loop principale dell'applicazione"""
        while True:
            self.visualizza_menu()
            
            try:
                scelta = input("\n👉 Inserisci la tua scelta (1-12): ").strip()
                
                if scelta == "1":
                    self.visualizza_sezione("parametri_personali")
                elif scelta == "2":
                    self.visualizza_sezione("parametri_aziendali")
                elif scelta == "3":
                    self.visualizza_sezione("parametri_fiscali_contabili")
                elif scelta == "4":
                    self.visualizza_sezione("parametri_bancari_finanziari")
                elif scelta == "5":
                    self.visualizza_sezione("parametri_legali_contrattuali")
                elif scelta == "6":
                    self.visualizza_sezione("parametri_sicurezza_privacy")
                elif scelta == "7":
                    self.modifica_parametro()
                elif scelta == "8":
                    self.cerca_parametro()
                elif scelta == "9":
                    self.esporta_agenda()
                elif scelta == "10":
                    self.importa_agenda()
                elif scelta == "11":
                    self.genera_report()
                elif scelta == "12":
                    print("\n👋 Arrivederci! Agenda salvata.")
                    break
                else:
                    print("❌ Scelta non valida. Inserisci un numero tra 1 e 12")
                
            except KeyboardInterrupt:
                print("\n\n👋 Applicazione interrotta dall'utente")
                break
            except Exception as e:
                print(f"❌ Errore: {e}")


def main() -> None:
    """Funzione principale"""
    print("\n🚀 Avvio Sistema di Gestione Agenda Completa...\n")
    
    manager = AgendaManager("agenda_parametri.json")
    manager.esegui()


if __name__ == "__main__":
    main()
