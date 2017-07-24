#!/usr/bin/env python3

import argparse
import os
import sys
from typing import Optional

from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.IO.parsing_settings.setting_parser import ModelsSettingsParser, KeysSettingsParser, SettingsParserMapper
from tilde.IO.input_format import KnowledgeBaseFormat, KnowledgeBaseFormatException
from tilde.representation.example import InternalExampleFormat, InternalExampleFormatException
from tilde.run.run_keys import run_keys
from tilde.run.run_models import run_models
from tilde.trees.TreeBuilder import TreeBuilderType

kb_suffix = '.kb'
bg_suffix = '.bg'
s_suffix = '.s'


class ProgramSettings:
    def __init__(self):
        self.debug_parsing = False  # type: bool
        self.kb_format = None  # type: Optional[KnowledgeBaseFormat]
        self.internal_examples_format = InternalExampleFormat.CLAUSEDB  # type: InternalExampleFormat
        self.filename_prefix = ""  # type: str
        self.use_bg = False  # type: bool
        self.treebuilder_type = TreeBuilderType.DETERMINISTIC  # type: TreeBuilderType

    @staticmethod
    def make_program_settings(arguments) -> 'ProgramSettings':
        settings = ProgramSettings()

        # get the name of the logic program
        fname_prefix = arguments.file
        # check if this file actually exists
        possible_kb_fname = fname_prefix + kb_suffix
        possible_s_fname = fname_prefix + s_suffix

        if not os.path.isfile(possible_kb_fname):
            raise FileNotFoundError("Could not find knowledge base file: " + possible_kb_fname)
        if not os.path.isfile(possible_s_fname):
            raise FileNotFoundError("Could not find settings file: " + possible_s_fname)
        # we now know there exist a kb and s file
        settings.filename_prefix = fname_prefix
        # is there a bg file?
        possible_bg_fname = fname_prefix + bg_suffix
        settings.use_bg = os.path.isfile(possible_bg_fname)

        if arguments.debug:
            settings.debug_parsing = True

        input_format = arguments.format
        print(input_format)
        if input_format == 'k' or input_format == 'key' or input_format == 'keys':
            settings.kb_format = KnowledgeBaseFormat.KEYS
        elif input_format == 'm' or input_format == 'model' or input_format == 'models':
            settings.kb_format = KnowledgeBaseFormat.MODELS
        else:
            raise Exception("required argument for --format has to be k/key(s) or m/model(s)")

        if arguments.ex:
            internal_examples_format = arguments.ex
            if internal_examples_format == 'c' or internal_examples_format == 'clausedb':
                settings.internal_examples_format = InternalExampleFormat.CLAUSEDB
            elif internal_examples_format == 's' or internal_examples_format == 'simpleprogram':
                settings.internal_examples_format = InternalExampleFormat.SIMPLEPROGRAM
            else:
                raise Exception('Got unknown input for argument internal example format: ' + str(arguments.ex))

        if arguments.mle:
            settings.treebuilder_type = TreeBuilderType.MLEDETERMINISTIC

        return settings


def make_cli_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()  # type: argparse.ArgumentParser
    # parser.parse_args('-v', '--verbose', help='helps increase verbosity',
    #                   action='store_true')

    parser.add_argument('file', help=("Filename prefix to the first order logic files."
                                      "Both the knowledge base ('*.kb') and settings ('*.s') files "
                                      "have to have the same name."))

    parser.add_argument('format', help=('Used to explicitly specify the format of the input knowledge base.'
                                        ' This can be key/k or models/m'),
                        choices=['m', 'model', 'models', 'k', 'key', 'keys'])

    parser.add_argument('-e', '--ex', help=('Used to explicitly specify how the examples have to be stored internally.'
                                            'This can be clausedb or simpleprogram. Normally, clausedb is faster.'),
                        choices=['c', 'clausedb', 's', 'simpleprogram'])

    parser.add_argument('-d', '--debug', help='Use debug mode',
                        action='store_true')

    parser.add_argument('--mle', help='Use MLE if possible',
                        action='store_true')
    return parser


def run_program(settings: ProgramSettings):
    # get the name of the program to run
    fname_labeled_examples = settings.filename_prefix + kb_suffix
    fname_settings = settings.filename_prefix + s_suffix

    # BACKGROUND KNOWLEDGE
    if settings.use_bg:
        fname_background_knowledge = settings.filename_prefix + bg_suffix
        background_knowledge = parse_background_knowledge(fname_background_knowledge)
    else:
        background_knowledge = None

    debug_printing = settings.debug_parsing

    if settings.kb_format is None:
        raise NotImplementedError('Automatic recognition of input format is not yet supported.')
    else:
        # SETTINGS FILE
        settings_file_parser = SettingsParserMapper.get_settings_parser(settings.kb_format)
        parsed_settings = settings_file_parser.parse(fname_settings)

    if settings.kb_format is KnowledgeBaseFormat.MODELS:
        run_models(fname_labeled_examples, parsed_settings, settings.internal_examples_format, settings.treebuilder_type, background_knowledge, debug_printing)
    elif settings.kb_format is KnowledgeBaseFormat.KEYS:
        run_keys(fname_labeled_examples, parsed_settings, settings.internal_examples_format, settings.treebuilder_type, background_knowledge, debug_printing)
    else:
        raise KnowledgeBaseFormatException('Only the input formats Models and Key are supported.')


def main(argv=sys.argv[1:]):
    argparser = make_cli_argument_parser()  # type: argparse.ArgumentParser
    cli_arguments = argparser.parse_args(argv)
    program_settings = ProgramSettings.make_program_settings(cli_arguments)
    run_program(program_settings)


if __name__ == '__main__':
    main()
