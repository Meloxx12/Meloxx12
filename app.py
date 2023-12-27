from Utils.calculos import quantity_energy, get_stamp, get_stamp_sodium, get_stamp_fattrans
from Querys.get_data import get_nutritional_data, get_formulation
from plots import get_plot_stamp, get_plot_reference_values
from presentacion import presentation
from InputValues import get_values
import pandas as pd


# Tabla de presentación
table = presentation()
print(table)


print('\n')

message_start = '''
Opciones:
\n 1. Busqueda en base de datos
\n 2. Realizar nueva formulación
\n 3. Cálculos en función de la composición nutricional del alimento
\n 4. salir'''



code_run = True
while code_run:

    print(message_start)

    print('\n')
    option = int(input('Ingrese la opción que desea realizar: '))

    if option == 1:

        search = True
        while search:

            name_food = str(input('''
            \n Ingrese el nombre del alimento a buscar (Ingrese salir para terminar la busqueda): '''))

            if name_food.capitalize() == 'Salir':
                search = False
            else:
                nutritional_data = get_nutritional_data(name_food = name_food)
                print(nutritional_data)
        
        print(message_start)
        print('\n')
        option = int(input('Ingrese la opción: '))

    elif option == 2:

        value = True
        while value:
            
            message = '''
            \n 1. Busqueda en base de datos
            \n 2. Crear formulación
            \n 3. Salir
            '''
            print(message)

            option = int(input('Ingrese la opción que desea: '))

            print('\n')

            if option == 1:
                search = True

                while search:

                    name_food = str(input('''
                    \n Ingrese el nombre del alimento a buscar (Ingrese salir para terminar la busqueda): '''))

                    if name_food.capitalize() == 'Salir':
                        search = False
                    else:
                        nutritional_data = get_nutritional_data(name_food = name_food)
                        print(nutritional_data)
        
            elif option == 2:
                food_ids = tuple(input("Ingrese los id's de los ingredientes: " ).split(','))

                df_formulation = get_formulation(food_ids = food_ids) # áca obtengo el dataframe con los ingredientes seleccionados

                names_ingredients = df_formulation['Nombre'].to_list()
                portions = []
                df_test = []
                

                bache, serving_size = map(float, input('Ingrese el bache a producir (gr) y el tamaño por servicio (gr): ').split(','))

            
                for i in range(len(names_ingredients)):
                    portion = float(input(f'Ingrese la cantidad en gramos para {names_ingredients[i]}: '))
                    portions.append(portion)
                

                for i in range(len(df_formulation)):
                    df_test.append(df_formulation.iloc[i][2:]*portions[i]/100)

                result = pd.DataFrame(data = df_test).sum()

                print(result)
            
            elif option == 3:
                value = False


    elif option == 3:

        # Áca obtengo el diccionario (contiene los valores que ingreso el usuario):
        nutritional_information = get_values()

        energy_sugar, energy_fatsat, energy_fattrans = quantity_energy(

                sugar = nutritional_information.get('Azúcares añadidos (gr)'),
                fat_sat = nutritional_information.get('Grasa saturada (gr)'),
                fat_trans = nutritional_information.get('Grasa trans (mg)')
            )

        message = print('''
        Opciones:
        \n 1.Determinar la existencia de sellos en el alimento
        \n 2.Visualizar la existencia de sellos
        \n 3.Visualizar valores de referencia''')

        print('\n')
        option = int(input('Ingrese la opción: '))

        if option == 1:
    
            value_bool_sugar = get_stamp(
                quantity_energy = energy_sugar,
                kcalByPortion = nutritional_information.get('Kcal por porción'),
                nutrient = nutritional_information.get('Azúcares añadidos (gr)')
            )
            
            value_bool_fat = get_stamp(
                quantity_energy = energy_fatsat,
                kcalByPortion = nutritional_information.get('Kcal por porción'),
                nutrient = nutritional_information.get('Grasa saturada (gr)')
            )

            value_bool_sodium = get_stamp_sodium(
                sodio = nutritional_information.get('Sodio (mg)'),
                kcalByPortion = nutritional_information.get('Kcal por porción')
            )

            value_bool_fattrans = get_stamp_fattrans(
                quantity_energy = energy_fattrans,
                kcalByPortion = nutritional_information.get('Kcal por porción'),
                nutrient = nutritional_information.get('Grasa trans (mg)')
            )
            
            if value_bool_sugar:
                print('\033[1m -Exceso en azùcares, debe contener el sello de advertencia\033[0m')
            else:
                print('No debe tener el sello de exceso en azúcares añadidos')
                
            if value_bool_fat:
                print('\033[1m -Exceso en grasas saturadas, debe contener el sello de advertencia\033[0m')
            else:
                print('No debe tener el sello de exceso en grasas saturadas')

            if value_bool_sodium:
                print('\033[1m -Exceso en sodio, debe contener el sello de advertencia\033[0m')
            else:
                print('No debe tener el sello de exceso en sodio')
            
            if value_bool_fattrans:
                print('\033[1m -Exceso en grasas trans, debe contener el sello de advertencia\033[0m')
            else:
                print('No debe tener el sello de exceso en grasas trans')

        elif option == 2:
            
            grafica = get_plot_stamp(
                sodium = nutritional_information.get('Sodio (mg)'),
                calories_portion = nutritional_information.get('Kcal por porción'),
                name_food = nutritional_information.get('Nombre'),
                portions = nutritional_information.get('Número de porciones consumidas'),
                energy_sugar = energy_sugar, 
                energy_fatsat = energy_fatsat,
                energy_fattrans = energy_fattrans)

        elif option == 3:
            
            nutritional_information = get_values()

            plot = get_plot_reference_values(

                portions = nutritional_information.get('Número de porciones consumidas'),
                calories_by_portion = nutritional_information.get('Kcal por porción'),
                total_fat = nutritional_information.get('Grasa total (gr)'),
                total_carbh = nutritional_information.get('Carbohidratos totales (gr)'),
                dietary_fiber = nutritional_information.get('Fibra (gr)'),
                protein = nutritional_information.get('Proteina (gr)'),
                sodium = nutritional_information.get('Sodio (mg)'),
                fat_sat = nutritional_information.get('Grasa saturada (gr)'),
                fat_trans = nutritional_information.get('Grasa trans (mg)'),
                sugar = nutritional_information.get('Azúcares añadidos (gr)')
            )

    elif option == 4:
        code_run = False
    

    
  
      

        






    



    


    