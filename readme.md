# Retail RecBole

Questo repository contiente l’implementazione di alcuni modelli presenti
nella libreria RecBole adattati ad un contesto Retail. Al progetto è
strutturato nel seguente modo:

- `raw_data`: In questa cartella ci sono i dati grezzi, non ancora
  processati per essere utilizzati dalla libreria. **Inserire in questa
  cartella i file `lines_hier.pkl` e `products.pkl`**
- `RECEIPT_LINES`: Cartella contente i dati che la libreria utilizza per
  addestrare e testare i modelli
- `model_type_1`: All’interno di questa cartella sono presenti tutti i
  notebook per addestrare ed eseguire i modelli. Qui verranno create le
  cartelle per il salvataggio dei modelli.

# File importanti

- `dataset_creation.ipynb`: Questo file adatta il formato dei dati
  presenti nella cartella `raw_data` al formato preso in input dalla
  libreria.
- `config.yaml`: File di configurazione generale dei modelli. **Se non
  funziona qualcosa probabilmente il problema è qui.** Qui vanno
  specificati i path del dataset, gli iperparametri del modello, le
  metriche da calcolare, numero di epoche, etc.

Per ogni modello è stato creato un notebook. Basta eseguirlo tutto per
addestrare e testare lo stesso. I risultati vengono salvati in un
cartella che si chiama “results”.
