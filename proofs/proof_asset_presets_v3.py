from forge.generator import generate_bpy_script

def main():
    print("--- Generated Blender Python script for bookshelf_large ---")
    bookshelf_script_content = generate_bpy_script(
        asset_name="bookshelf_large_test",
        preset_name="bookshelf_large",
        output_path="path/to/bookshelf_large.obj" # Placeholder path
    )
    print(bookshelf_script_content)
    print("
" + "="*80 + "
")

    print("--- Generated Blender Python script for pillar_round ---")
    pillar_script_content = generate_bpy_script(
        asset_name="pillar_round_test",
        preset_name="pillar_round",
        output_path="path/to/pillar_round.obj" # Placeholder path
    )
    print(pillar_script_content)
    print("
" + "="*80 + "
")

    print("Proof file execution complete. Please manually inspect the generated Blender Python scripts above.")

if __name__ == "__main__":
    main()
