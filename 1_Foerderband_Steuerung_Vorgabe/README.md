Quellcode Vorgabe für die Steuerungsentwicklung des Förderbandes
================================================================

In diesem Projekt finden Sie alle nötigen Sourcen, um später die Steuerung des Förderbandes in Betrieb zu nehmen. An ein
paar wenigen Stellen gibt es aber noch ein bisschen etwas zu tun. In dieser Beschreibung sollten Sie alles finden, um
sich in diesem Projekt zurechtzufinden. Sollten Sie einmal gar nicht weiter kommen, schauen Sie sich die Abschnitte "
Hinweise, die beim Verständnis helfen können" und "Wichtig zu beachten" weiter unten an - vielleicht gibt es dort schon
eine Antwort auf Ihre Frage.

Wie Sie einsteigen können
-------------------------

Schauen Sie sich in den Folien nochmal an, welche Module wir definiert haben. Alle Blöcke, welche im Klassendiagramm
dargestellt sind, finden Sie nun wieder als eigene Datei und damit als eigene Klasse.

Nun können Sie die Datei test.py ausführen und schauen, welche Tests schon durchlaufen (der EncoderTest ist bereits
vollständig und korrekt implementiert) und welche noch Fehler zeigen (der PIDControllerTest läuft noch nicht durch, weil
die entsprechenden Funktionen und auch die korrekten Testvektoren noch nicht eingesetzt wurden.).

Um die Regelung später auf dem tatsächlichen Förderband laufen zu lassen (natürlich, nachdem Sie den PIDController
korrekt implementiert haben), können Sie den gesamten Code auf das RaspberryPi kopieren und dort Main.py ausführen.

Wo es etwas zu tun gibt
-----------------------

Das Meiste in diesem Projekt ist schon für Sie vorbereitet. Es gibt aber noch ein paar wenige Stellen, wo Sie selbst
entsprechende Ergänzungen machen müssen:

* In der Datei Main.py gibt es folgende Stellen:

    * implementieren Sie die Schritte gemäss TODO in der IRQ-Funktion
      ``timerPinIRQ()``. Diese Funktion wird im 100Hz-Takt aufgerufen, um die eigentlich Regelung zu implementieren
    * ergänzen Sie die Zeilen in ``startPressed()`` und ``stopPressed()`` um den Motor zu starten bzw. zu stoppen

* In der Datei PIDController.py gibt es folgende Stellen:

    * in der Funktion ``calculateTargetValue()`` müssen noch die vollständige Implementierung des PID-Controllers
      einfüllen

* In der Datei tests/PIDControllerTest.py müssen Sie

Hinweise die beim Verständnis helfen können
-------------------------------------------

* Die Klasse ``PIDControllerTest`` ist von ``TestCase`` abgeleitet und erlaubt dadurch, eine Reihe von Testfunktionen
  aus dem Python-Unittesting Framework zu nutzen. Dies machen wir uns beim Aufruf der
  Funktion ``assertEqual(expected_value, actual_value)`` zunutze.
* Auf Computer-Systemen können Fliesspunktzahlen (floating-point-values) häufig nicht präzise dargestellt werden. Dies
  äussert sich dann darin, dass plötzlich Werte wie 15.00000000000000001 auftauchen, wo eigentlich 15.0 stehen müsste.
  Solche Ungenauigkeiten interessieren uns aber meistens nicht, da wir mit viel weniger Genauigkeit arbeiten.

  Um diese Probleme aber in den Tests sauber abzudecken, können wir statt ``assertEqual()`` die
  Funktion ``assertAlmostEqual()`` nutzen. Mit dieser Funktion können wir zum Beispiel in unserem Fall klar festhalten,
  dass wir uns nur für eine Genauigkeit von 3 Stellen nach dem Komma interessieren.

Wichtig zu beachten
-------------------

* Stellen Sie sicher, dass Sie das gesamte Projekt in einen eigenen Ordner ausgepackt haben und das Projekt als solches
  in PyCharm geöffnet haben. Andernfalls kann es sein, dass Python nicht alle benötigten Dateien am richtigen Ort
  findet.
* Wenn Sie das Projekt richtig entpackt haben, sollten alle Dateien vorhanden und am richtigen Ort abgelegt worden sein
  \- Sie sollten keine neuen Dateien anlegen müssen und auch keine Dateien verschieben müssen.

