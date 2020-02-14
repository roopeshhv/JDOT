# Copyright (c) 2020 Nutanix Inc. All rights reserved.
#
#
"""
A foundationable node abstraction.
"""

SUPPORTED_HYPERVISORS = ["kvm", "esx", "hyperv", "xen", "phoenix", "linux"]


class FoundationNode(object):
  """
  A foundationable node abstraction.
  """

  def __init__(self, metadata):
    """

    Args:
      metadata (dict): metadata about the node from jarvis.
    """
    self.metadata = metadata["data"]
    self.hyp_type = None
    self._hardware_attributes_override = {}
    self.image_now = True
    self.ipv6 = None
    self.compute_only = False

  @property
  def network(self):
    """

    Returns:
      (str)
    """
    return self.metadata["network"]

  @property
  def netmask(self):
    """

    Returns:
      (str)
    """
    return self.network["svm_subnet_mask"]

  @property
  def gateway(self):
    """

    Returns:
      (str)
    """
    return self.network["default_gw"]

  @property
  def svm_ip(self):
    """

    Returns:
      (str)
    """
    return self.metadata["svm_ip"]

  @property
  def cvm_ip(self):
    """

    Returns:
      (str)
    """
    return self.svm_ip

  @property
  def host_ip(self):
    """

    Returns:
      (str)
    """
    return self.metadata["hypervisor"]["ip"]

  @property
  def ipmi_ip(self):
    """

    Returns:
      (str)
    """
    print self.metadata
    print type(self.metadata)
    return self.metadata["power_mgmt"]["ipmi"].get("ip", None)

  @ipmi_ip.setter
  def ipmi_ip(self, value):
    """
    Set the ipmi ip to value.

    Args:
      value(str): IPMI IP.


    """
    self.metadata["power_mgmt"]["ipmi"]["ip"] = value

  @property
  def ipmi_mac(self):
    """

    Returns:
      (str)
    """
    return self.metadata["power_mgmt"]["ipmi"].get("network_mac_addr", None)

  @property
  def ipmi_gateway(self):
    """

    Returns:
      (str)
    """
    return (self.metadata["power_mgmt"]["ipmi"].get("default_gateway", None) or
            self.network["default_gw"])

  @property
  def ipmi_netmask(self):
    """

    Returns:
      (str)
    """
    return (self.metadata["power_mgmt"]["ipmi"].get("netmask", None) or
            self.network["svm_subnet_mask"])

  @property
  def ipmi_user(self):
    """

    Returns:
      (str)
    """
    return self.metadata["power_mgmt"]["ipmi"]["user"]

  @property
  def ipmi_password(self):
    """

    Returns:
      (str)
    """
    return self.metadata["power_mgmt"]["ipmi"]["passwd"]

  @property
  def block_id(self):
    """

    Returns:
      (str)
    """
    #return self.metadata["hardware"]["block_id"]
    return "manual"

  @property
  def position(self):
    """

    Returns:
      (str)
    """
    return self.metadata["hardware"]["position"]

  @property
  def serial(self):
    """

    Returns:
      (str)
    """
    return self.metadata["hardware"]["serial"]

  @property
  def hostname(self):
    """

    Returns:
      (str)
    """
    return self.network["hostname"]

  @hostname.setter
  def hostname(self, new_name):
    """
    Set the hostname to new_name.

    Args:
      new_name(str): hostname.

    """
    self.network["hostname"] = new_name

  @property
  def add_compute_only(self):
    """
    Returns:
      (bool) : Node to set as compute only.
    """
    return self.compute_only

  @add_compute_only.setter
  def add_compute_only(self, compute_only):
    """
    Adds node as compute only
    Args:
      compute_only(bool) : True to set the node as compute only.
    """
    self.compute_only = compute_only


  @property
  def hypervisor_type(self):
    """

    Returns:
      (str): Hypervisor type to which the node has to be imaged.
    """
    return self.hyp_type

  @hypervisor_type.setter
  def hypervisor_type(self, value):
    """
    Set the hypervisor type for the node.

    Args:
      value(str): Hypervisor type.

    Raises:
      AssertionError: If hypervisor type is not supported.

    Returns:
      None
    """
    assert value in SUPPORTED_HYPERVISORS, (
      "Hypervisor type must be one of %s" % SUPPORTED_HYPERVISORS)
    self.hyp_type = value

    @property
    def ipv6(self):
      """

      Returns:
        (str): IPv6 value for the node
      """
      return self.ipv6

    @ipv6.setter
    def ipv6(self, value):
      """
      Set the IPv6 value for the node.

      Args:
        value(str): IPv6 address

      """

      self.ipv6 = value

  @property
  def hardware_attributes_override(self):
    """

    Returns:
      (dict): Dictionary containing hardware attributes to be set on the node.
    """
    return self._hardware_attributes_override

  def add_hardware_attribute(self, key, value):
    """
    Adds a hardware attribute to the node.

    Args:
      key(str): Hardware attribute key.
      value(object): Value of the hardware attribute.
    """
    self._hardware_attributes_override[key] = value

