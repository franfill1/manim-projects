# Fugassa Cup 2021 - Exercise 20
Animation of the solution to an exercise from **Fugassa Cup**, a team-based math competition that took place on 22th November 2021, hosted by phiquadro.it

[Link to the presentation](https://franfill1.github.io/manim-projects/fugassa_cup_ex/Fugassa%20Cup%202021%20-%20Exercise%2020/)
## Exercise description (ITA)

**Regionale 12480**  
Badda: - Oh no, Mattysal si è perso! Sono le 22:33 e il treno doveva partire 3 minuti fa.  -  
*Ma voi lo sapevate perch ́e era fermo? No, davvero? Ora ve lo raccontiamo! Nel mentre, Chot trova finalmente Mattysal!*  
Chot: - Vieni, stiamo per partire! -  
Mattysal: - Ma perch ́e siete così silenziosi? -  
*Badda prega Mattysal di fare silenzio perch ́e non aveva nessuna voglia di discutere con un controllore di Trenitalia.*  
Badda: (parlando a bassa voce) - Abbiamo causato il ritardo di un treno! E tipo illegalissimo! -  
Mattysal: (parlando ad alta voce) - Ma come hai fatto? -  
Badda: - Mi sono messo in mezzo alle porte coprendo i sensori, affinchè queste non si chiudessero. Per farti capire meglio, c’era un triangolo ABC e sul lato BC erano presi due punti X, Y tali che CA = CX e BA = BY . Detti M,N i punti medi di AX e
AY , i sensori erano proprio M,N. Io mi trovavo esattamente nel punto V (come ’Valebadda’) che era l’intersezione tra CM e
BN, e l’angolo ∠MVA valeva... Aspetta, non mi ricordo, so solo che ∠BAC = 86°, ∠ABC = 62°  
Mattysal: - Certo che in geometria sei scarso... io non ero sui sensori eppure so quanto valeva l’angolo, sulla base di ciò che mi hai detto. Non è questione di memoria! - Qual era questa ampiezza in gradi?  
*Improvvisamente, giunti a Lavagna, Guide scompare.*

## Render the animation yourself
```bash
cd fugassa_cup_ex
manim main.py --save_sections
manedit --quick_present_export media/videos/main/1080p60/sections/exercise.json --project_name "Fugassa Cup 2021 - Exercise 20"
cd "Fugassa Cup 2021 - Exercise 20"
python -m http.server
```
### requirements:
- [manim](https://github.com/ManimCommunity/manim)
- [manim editor](https://github.com/ManimCommunity/manim_editor)