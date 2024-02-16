import sphinx
from docutils import nodes
from docutils.parsers.rst import directives
from rosidl_adapter.parser import parse_message_string
from sphinx.util.docutils import SphinxDirective


def nonempty_string(option):
    if option is None:
        raise ValueError("Argument is required.")
    if not isinstance(option, str):
        return TypeError("Argument must be a string.")
    if option == "":
        raise ValueError("Argument must not be empty.")

    return option


class RosMessage(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        "pkg_name": nonempty_string,
        "msg_name": nonempty_string,
    }

    def run(self):
        path = directives.uri(self.arguments[0])

        if "pkg_name" not in self.options:
            raise ValueError("Option \"pkg_name\" is required.")

        if "msg_name" not in self.options:
            raise ValueError("Option \"msg_name\" is required.")

        with open(path) as f:
            message_string = f.read()
        parsed_message = parse_message_string(self.options["pkg_name"], self.options["msg_name"], message_string)
        id = f"rosmessage-{self.env.new_serialno('rosmessage')}"
        par = nodes.section(ids=[id])
        title = nodes.title(text=parsed_message.msg_name)
        par += title

        for comment in parsed_message.annotations["comment"]:
            par += nodes.paragraph(text=comment)

        if len(parsed_message.constants) > 0:
            constants = nodes.section(ids=[id + "-constants"])
            constants += nodes.title(text="Constants")
            for constant in parsed_message.constants:
                constants.extend(self.document_constant(constant))
            par += constants

        if len(parsed_message.fields) > 0:
            fields_section = nodes.section(ids=[id + "-fields"])
            fields_section += nodes.title(text="Fields")
            for field in parsed_message.fields:
                fields_section.extend(self.document_field(field))

            par += fields_section

        return [par]

    def document_constant(self, constant):
        desc = sphinx.addnodes.desc()
        desc.document = self.state.document
        desc["domain"] = "ros"
        desc["objtype"] = "msg-constant"
        sig = sphinx.addnodes.desc_signature()
        sig += sphinx.addnodes.desc_type(text=constant.type)
        sig += sphinx.addnodes.desc_sig_space()
        sig += sphinx.addnodes.desc_name(text=constant.name)
        sig += sphinx.addnodes.desc_sig_space()
        sig += sphinx.addnodes.desc_sig_element(text=f"= {constant.value}")
        desc += sig
        comments = constant.annotations["comment"]
        if len(comments) > 0:
            content = sphinx.addnodes.desc_content()
            for comment in comments:
                content += nodes.paragraph(text=comment)
            desc += content
        return [desc]

    def document_field(self, field):
        desc = sphinx.addnodes.desc()
        desc["domain"] = "ros"
        desc["objtype"] = "msg-constant"
        sig = sphinx.addnodes.desc_signature()
        sig += sphinx.addnodes.desc_type(text=field.type)
        sig += sphinx.addnodes.desc_sig_space()
        sig += sphinx.addnodes.desc_name(text=field.name)
        # TODO: default value
        desc += sig
        comments = field.annotations["comment"]
        if len(comments) > 0:
            content = sphinx.addnodes.desc_content()
            for comment in comments:
                content += nodes.paragraph(text=comment)
            desc += content
        return [desc]


def setup(app):
    app.add_directive("rosmessage", RosMessage)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
