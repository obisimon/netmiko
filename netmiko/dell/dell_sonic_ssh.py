"""
Dell EMC PowerSwitch platforms running Enterprise SONiC Distribution by Dell Technologies Driver
- supports dellenterprisesonic.
"""
from netmiko.no_enable import NoEnable
from netmiko.cisco_base_connection import CiscoSSHConnection
from netmiko import log
import time


class DellSonicSSH(NoEnable, CiscoSSHConnection):
    """
    Dell EMC PowerSwitch platforms running Enterprise SONiC Distribution
    by Dell Technologies Driver - supports dellenterprisesonic.
    """

    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self._test_channel_read(pattern=r"[>$#]")
        # Clear the read buffer
        time.sleep(0.3 * self.global_delay_factor)
        self.clear_buffer()
        self._enter_shell()
        self.disable_paging()
        self.set_base_prompt(alt_prompt_terminator="$")

    def config_mode(
        self,
        config_command: str = "configure terminal",
        pattern: str = r"\#",
        re_flags: int = 0,
    ) -> str:
        return super().config_mode(
            config_command=config_command, pattern=pattern, re_flags=re_flags
        )

    def _enter_shell(self):
        """Enter the sonic-cli Shell."""
        log.debug("Enter sonic-cli Shell.")
        output = self.send_command("sonic-cli", expect_string=r"\#")
        return output

    def _return_cli(self):
        """Return to the CLI."""
        return self.send_command("exit", expect_string=r"\$")
