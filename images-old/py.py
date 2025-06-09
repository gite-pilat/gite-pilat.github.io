import os
from PIL import Image
import time

def compress_images_to_webp_smart(
    input_folder='.',
    output_folder='webp_images',
    min_original_size_kb=300, # Seulement les images > 300KB seront traitées
    target_max_size_mb=1,     # Cible < 1MB pour les images compressées
    initial_quality=95,       # Qualité de départ
    min_quality=70,           # Qualité minimale acceptable
    quality_step=5            # Pas de réduction de qualité
):
    """
    Compresse les images JPG d'un dossier vers le format WebP,
    ne traitant que celles dépassant une certaine taille initiale
    et visant une taille maximale après compression.

    Args:
        input_folder (str): Le chemin du dossier contenant les images JPG.
        output_folder (str): Le nom du dossier où sauvegarder les images WebP.
        min_original_size_kb (int): Taille minimale (en KB) de l'image JPG originale pour être traitée.
        target_max_size_mb (int): Taille maximale (en MB) que l'image WebP compressée doit atteindre.
        initial_quality (int): Qualité WebP de départ (0-100).
        min_quality (int): Qualité WebP minimale à ne pas descendre en dessous (0-100).
        quality_step (int): Valeur par laquelle réduire la qualité à chaque itération.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Dossier de sortie '{output_folder}' créé.")

    print(f"\nDébut du traitement des images JPG de '{input_folder}' vers WebP...")
    print(f"Seules les images de plus de {min_original_size_kb} KB seront compressées.")
    print(f"Tentative de compression pour que les images fassent moins de {target_max_size_mb} MB.")
    print(f"Qualité initiale: {initial_quality}, Qualité minimale: {min_quality}\n")

    converted_count = 0
    skipped_count = 0
    total_original_size_processed = 0
    total_compressed_size = 0

    target_max_size_bytes = target_max_size_mb * 1024 * 1024
    min_original_size_bytes = min_original_size_kb * 1024

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.webp'
            output_path = os.path.join(output_folder, output_filename)

            try:
                original_size = os.path.getsize(input_path)

                if original_size <= min_original_size_bytes:
                    print(f"Sautée '{filename}': Taille originale ({(original_size / 1024):.2f} KB) inférieure ou égale à {min_original_size_kb} KB.")
                    skipped_count += 1
                    continue

                total_original_size_processed += original_size
                converted_count += 1

                img = Image.open(input_path)
                current_quality = initial_quality
                compressed_size = float('inf') # Initialiser à une valeur haute

                print(f"Traitement de '{filename}' ({(original_size / 1024):.2f} KB)...")

                while compressed_size > target_max_size_bytes and current_quality >= min_quality:
                    try:
                        # Sauvegarder temporairement pour vérifier la taille
                        temp_output_path = output_path + ".tmp"
                        img.save(temp_output_path, "webp", quality=current_quality)
                        compressed_size = os.path.getsize(temp_output_path)

                        if compressed_size > target_max_size_bytes and current_quality > min_quality:
                            print(f"  Qualité {current_quality}: {(compressed_size / (1024*1024)):.2f} MB (trop grand). Réduction de la qualité...")
                            current_quality -= quality_step
                        elif compressed_size <= target_max_size_bytes:
                            print(f"  Cible atteinte à qualité {current_quality}: {(compressed_size / (1024*1024)):.2f} MB.")
                            os.rename(temp_output_path, output_path) # Renommer le fichier final
                            total_compressed_size += compressed_size
                            break # Sortir de la boucle while
                        else: # Si on est à min_quality et toujours trop grand
                            print(f"  Qualité {current_quality} atteinte: {(compressed_size / (1024*1024)):.2f} MB (dépasse {target_max_size_mb} MB). Sauvegarde avec cette qualité.")
                            os.rename(temp_output_path, output_path)
                            total_compressed_size += compressed_size
                            break
                    except Exception as e_inner:
                        print(f"  Erreur lors de la tentative de compression à qualité {current_quality}: {e_inner}")
                        if os.path.exists(temp_output_path):
                            os.remove(temp_output_path)
                        break # Sortir de la boucle en cas d'erreur de compression

                if current_quality < min_quality and compressed_size > target_max_size_bytes:
                     print(f"  Attention : Impossible d'atteindre la cible de {target_max_size_mb} MB pour '{filename}' même à la qualité minimale ({min_quality}).")
                     print(f"  Sauvegardé avec une taille de {(compressed_size / (1024*1024)):.2f} MB.")
                
                img.close() # Important de fermer l'image pour libérer les ressources

            except FileNotFoundError:
                print(f"Erreur : Le fichier '{filename}' n'a pas été trouvé.")
            except Exception as e:
                print(f"Erreur inattendue lors du traitement de '{filename}': {e}")
    
    print("\n---------------------------------------------------")
    print(f"Traitement terminé.")
    print(f"{converted_count} image(s) traitée(s) et convertie(s).")
    print(f"{skipped_count} image(s) ignorée(s) (déjà petite).")
    
    if total_original_size_processed > 0:
        overall_reduction_percent = ((total_original_size_processed - total_compressed_size) / total_original_size_processed) * 100 if total_original_size_processed > 0 else 0
        print(f"Taille totale des JPG traités : {(total_original_size_processed / (1024*1024)):.2f} MB")
        print(f"Taille totale des WebP générés : {(total_compressed_size / (1024*1024)):.2f} MB")
        print(f"Réduction de taille globale sur les images traitées : {overall_reduction_percent:.2f}%")
    else:
        print("Aucune image JPG/JPEG de taille suffisante trouvée pour être traitée.")
    print("---------------------------------------------------\n")

if __name__ == "__main__":
    # Utilisation par défaut
    compress_images_to_webp_smart()

    # Exemple d'utilisation avec des paramètres personnalisés :
    # compress_images_to_webp_smart(
    #     input_folder='./grandes_photos',
    #     output_folder='./photos_web_optimisees',
    #     min_original_size_kb=500,  # Ne traiter que les images > 500KB
    #     target_max_size_mb=0.5,    # Cible les images < 500KB
    #     initial_quality=90,
    #     min_quality=60
    # )