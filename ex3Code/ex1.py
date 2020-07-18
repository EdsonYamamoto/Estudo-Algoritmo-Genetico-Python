# coding: utf-8
import os
import re

template_int = """
// seu template aqui ..
namespace umanamespace.umdominio
{
    public interface IumaentidadesController : IControllerBase<umaentidade>
    {
        
    }
}
"""

template_imp = """
namespace umanamespace.umdominio.Impl
{
    public class umaentidadesController : ControllerBase<umaentidade>, IumaentidadesController
    {
        private readonly IumaentidadeService service;
        public umaentidadesController(IumaentidadeService service) : base(service)
        {
            this.service = service;
        }
    }
}
"""

def multiple_replacer(*key_values):
    replace_dict = dict(key_values)
    replacement_function = lambda match: replace_dict[match.group(0)]
    pattern = re.compile("|".join([re.escape(k) for k, v in key_values]), re.M)
    return lambda string: pattern.sub(replacement_function, string)

def multiple_replace(string, *key_values):
    return multiple_replacer(*key_values)(string)

# subdominios em dominios
subdomains = ['pasta1', 'pasta2', 'pasta3']

# templates 

# #################
# Funcoes do script #
# #################

def create_temp_folder():
    # Cria subpastas e dicionario com paths
    temp_folder = 'temp_controllers'
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    for subdomain in subdomains:
        folder = temp_folder+ '/' + subdomain
        if not os.path.exists(folder):
            os.makedirs(folder)


def create_file(nome, template, dominio, entidade):
    #s = template.replace('umdominio', dominio)
    #s = template.replace('umaentidade', entidade)

    replacements = ("umdominio", dominio), ('umaentidade', entidade)
    s = multiple_replace(template, *replacements)

    file = open(nome, 'w')
    file.write(s)
    file.close()

def getEntities(path):
    entities = list()
    for file in os.listdir(path):
        if 'Entity' in file:
            continue
        entities.append(file.replace('.cs',''))
    return entities

contexts = {
    'Pasta1':{
        'entities': getEntities('pasta1/Entities'),
    },
    'Pasta2': {
        'entities': getEntities('pasta2/Entities'),
    },
    'Pasta3': {
        'entities': getEntities('pasta3/Entities'),
    },
}


if __name__ == "__main__":
    # Cria pasta temporaria se necessario
    print('\t')
    create_temp_folder()
    for context in contexts.keys():
        for entity in contexts[context]['entities']:
            print(entity, end='\t\t')
        print('\n')