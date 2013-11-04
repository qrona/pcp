(ns pcp.data
  "Dataset -> matrix conversion. Each column is
the grayscale image"
  (:require [incanter.core :as incanter]
            [incanter.io :as incanter-io])
  (:use [clojure.java.io :as io])
  (:import [javax.imageio ImageIO]
           [javax.swing JFrame JPanel]
           [java.awt.image BufferedImage]
           [java.awt Color]
	   [java.io FileOutputStream]))

(defn bmp->pixels
  [bmp-data]
  (let [w (.getWidth bmp-data)
        h (.getHeight bmp-data)]
    (for [i (range w)
          j (range h)]
      (let [rgb-int (.getRGB bmp-data i j)
            r       (bit-and (bit-shift-right rgb-int 16)
                             0xFF)
            g       (bit-and (bit-shift-right rgb-int 8)
                             0xFF)
            b       (bit-and rgb-int 0xFF)]
        (list r g b)))))

(defn rgb->grayscale
  [[r g b]]
  (/ (+ r g b) 3))

(defn read-bmp
  "bmp-filename -> rgb array"
  [filename]
  (-> filename
      io/input-stream
      ImageIO/read
      bmp->pixels))

(defn bmp->pixel-column
  "bmp-filename -> grayscale"
  [filename]
  (let [pixels (read-bmp filename)]
   (map rgb->grayscale pixels)))

(defn directory->pixel-columns
  [directory]
  (map
   bmp->pixel-column
   (rest
    (map str (file-seq (io/file directory))))))

(defn pixel-columns->matrix
  [pixel-columns]
  (incanter/trans
   (incanter/matrix pixel-columns)))

(defn directory->csv
  "A directory of images is converted to
a csv file with grayscale values"
  [directory csv]
  (let [data (pixel-columns->matrix
              (directory->pixel-columns directory))]
    (println "Initiating save")
    (flush)
    (incanter/save data csv)))

(defn load-csv
  "We expect the CSV file to contain a bitmap
image row-wise. User is expected to serve the
image dimensions."
  [a-csv-file]
  (let [lines (-> a-csv-file
                  clojure.java.io/reader
                  line-seq)]
    (incanter/matrix
     (map
      #(map
        (fn [a-str] (java.lang.Double/parseDouble a-str))
        (clojure.string/split % #"\s+"))
      lines))))

(defn show-img
  [img w h]
  (let [jframe  (JFrame. "Escalator")
        display (proxy [JPanel] []
                  (paintComponent
                    [g]
                    (.drawImage g img 0 0 nil)))]
    (doto jframe
      (.setResizable false)
      (.add display)
      (.pack)
      (.setSize w h)
      (.setVisible true))))

(defn row->render
  [grayscale-values w h]
  (let [img (BufferedImage. w h BufferedImage/TYPE_USHORT_GRAY)]
    (doseq [i (range w)
            j (range h)]
     (.setRGB img i j (nth grayscale-values (+ i (* j w)))))
    img))

(defn -main
  [& args]
  (directory->csv (first args) (FileOutputStream. (second args))))
